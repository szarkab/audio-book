#!/usr/bin/env python3
"""Prepare the pinned Hungarian checkpoint without materializing all F32 weights.

Developer-only preparation. The application consumes the finished local model
and never downloads or converts checkpoints during narration.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import time

import mlx.core as mx
from mlx.utils import tree_flatten
from huggingface_hub import HfApi, snapshot_download
from safetensors import safe_open
from mlx_audio.tts.models.vibevoice import Model, ModelConfig

SOURCE = "Cseti/VibeVoice_7B_hun_v2"
SOURCE_REVISION = "22434d6f261e2f231b3c358563bdf2d2e8caab57"
TOKENIZER = "Qwen/Qwen2.5-7B"
TOKENIZER_REVISION = "d149729398750b98c0af14eb82c78cfe92750796"


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def prepare(source: Path, output: Path, wait_for_source: bool = False):
    if output.exists():
        raise SystemExit("The target model already exists; use a new destination.")
    if not mx.metal.is_available():
        raise SystemExit("Apple GPU unavailable; preparation was not started.")
    config = json.loads((source / "config.json").read_text())
    index = json.loads((source / "model.safetensors.index.json").read_text())
    shards = sorted(set(index["weight_map"].values()))
    if not wait_for_source and not all((source / name).is_file() for name in shards):
        raise SystemExit("The pinned source download is not complete.")
    expected_bytes = int(index["metadata"]["total_size"])
    if shutil.disk_usage(output.parent).free < expected_bytes + 2_000_000_000:
        raise SystemExit("Insufficient space for conservative conversion workspace.")
    mx.set_default_device(mx.gpu)
    mx.set_cache_limit(512 * 1024 * 1024)
    remote = HfApi().model_info(SOURCE, revision=SOURCE_REVISION, files_metadata=True)
    source_hashes = {entry.rfilename: entry.lfs.sha256 for entry in remote.siblings if entry.lfs}
    model = Model(ModelConfig.from_dict(config))
    shapes = {name: value.shape for name, value in tree_flatten(model.parameters())}
    converted_keys = set()
    weight_map = {}
    hashes = {}
    total_bytes = 0
    started = time.perf_counter()
    with tempfile.TemporaryDirectory(dir=output.parent, prefix=".vibevoice-prepare-") as folder:
        target = Path(folder)
        snapshot_download(TOKENIZER, revision=TOKENIZER_REVISION, local_dir=target,
                          allow_patterns=["tokenizer.json", "tokenizer_config.json", "vocab.json",
                                          "merges.txt", "special_tokens_map.json"], max_workers=2)
        for number, shard in enumerate(shards, 1):
            deadline = time.monotonic() + 1800
            while not (source / shard).is_file():
                if not wait_for_source or time.monotonic() > deadline:
                    raise RuntimeError(f"Source download did not complete: {shard}")
                time.sleep(5)
            if digest(source / shard) != source_hashes[shard]:
                raise ValueError(f"Source checkpoint checksum mismatch: {shard}")
            converted = {}
            with safe_open(source / shard, framework="np") as reader:
                for key in reader.keys():
                    values = model.sanitize({key: mx.array(reader.get_tensor(key))})
                    if not values and "rotary_emb.inv_freq" not in key:
                        raise ValueError(f"Unmapped source weight: {key}")
                    for name, value in values.items():
                        if name in converted_keys or value.shape != shapes[name]:
                            raise ValueError(f"Duplicate or incompatible weight: {name}")
                        converted_keys.add(name)
                        language_weight = name.startswith("language_model.") or name == "lm_head.weight"
                        if language_weight and name.endswith(".weight") and value.ndim == 2:
                            q, scales, biases = mx.quantize(value.astype(mx.float16), group_size=64, bits=4)
                            converted[name] = q
                            converted[name[:-len("weight")] + "scales"] = scales
                            converted[name[:-len("weight")] + "biases"] = biases
                        else:
                            # Preserve the full Hungarian diffusion and both audio-codec branches.
                            converted[name] = value.astype(mx.float16) if language_weight else value
                        mx.eval(converted[name])
                        del value
            mx.eval(converted)
            destination = target / shard
            mx.save_safetensors(str(destination), converted)
            for name in converted:
                weight_map[name] = shard
                total_bytes += converted[name].nbytes
            hashes[shard] = digest(destination)
            print(f"Converted {number}/{len(shards)}: {shard}, {destination.stat().st_size / 1e9:.2f} GB", flush=True)
            del converted, values
            mx.clear_cache()
        missing = set(shapes) - converted_keys
        if missing:
            raise ValueError(f"Missing model weights: {sorted(missing)}")
        config["quantization"] = {"bits": 4, "group_size": 64, "mode": "affine"}
        config["torch_dtype"] = "float32"
        (target / "config.json").write_text(json.dumps(config, indent=2))
        (target / "model.safetensors.index.json").write_text(json.dumps({
            "metadata": {"total_size": total_bytes}, "weight_map": weight_map,
        }, indent=2))
        preparation = {
            "source": SOURCE, "source_revision": SOURCE_REVISION,
            "tokenizer": TOKENIZER, "tokenizer_revision": TOKENIZER_REVISION,
            "language_bits": 4, "group_size": 64, "audio_dtype": "float32",
            "source_weight_count": len(index["weight_map"]),
            "converted_parameter_count": len(converted_keys),
            "source_shard_sha256": source_hashes, "shard_sha256": hashes, "elapsed_seconds": time.perf_counter() - started,
        }
        (target / "preparation.json").write_text(json.dumps(preparation, indent=2))
        if (target / ".cache").exists():
            shutil.rmtree(target / ".cache")
        target.rename(output)
    print("MODEL_READY", str(output.resolve()), flush=True)


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=root / ".local/models/VibeVoice_7B_hun_v2-source")
    parser.add_argument("--output", type=Path, default=root / ".local/models/VibeVoice_7B_hun_v2-mlx-4bit")
    parser.add_argument("--wait-for-source", action="store_true")
    args = parser.parse_args()
    prepare(args.source, args.output, args.wait_for_source)
