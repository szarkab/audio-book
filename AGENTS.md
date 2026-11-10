# Agent instructions

## Agent skills

### Issue tracker

Issues and specs live in GitHub Issues for `szarkab/audio-book`. Before reading or writing tickets, read `docs/agents/issue-tracker.md`.

### Triage labels

Use the five default triage labels. Before assigning a triage status, read `docs/agents/triage-labels.md`.

### Domain docs

Single-context layout: root `GLOSSARY.md` and `docs/adr/`. Before exploring the codebase, read `docs/agents/domain.md`.

## Workspace cleanup

Keep the approved Piper Imre model and its active runtime. After validating a replacement, remove this project's retired model downloads, test app bundles, environments and generated probes. Preserve book sources, user-saved audio, unrelated projects and Git history. Keep historical findings as small documents, rather than retaining obsolete binaries and models.
