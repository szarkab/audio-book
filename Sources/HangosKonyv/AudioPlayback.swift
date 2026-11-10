import AVFAudio
import Foundation
import SwiftUI

@MainActor
final class AudioPlayback: NSObject, ObservableObject, AVAudioPlayerDelegate {
    @Published private(set) var isReady = false
    @Published private(set) var isPlaying = false
    @Published private(set) var elapsed: TimeInterval = 0
    @Published private(set) var duration: TimeInterval = 0
    @Published private(set) var error: String?
    @Published var volume: Double = 0.8 {
        didSet { player?.volume = Float(volume) }
    }
    private var player: AVAudioPlayer?
    private var timer: Timer?

    func load(_ url: URL) {
        clear()
        do {
            let audio = try AVAudioPlayer(contentsOf: url)
            audio.delegate = self
            audio.volume = Float(volume)
            guard audio.prepareToPlay() else {
                throw WorkerFailure(message: "Az MP3 nem készíthető elő lejátszásra.")
            }
            player = audio
            duration = audio.duration
            isReady = true
            // Loading a finished file never starts playback.
        } catch {
            self.error = "Az MP3 elkészült, de a lejátszó nem tudta megnyitni. A Finderből továbbra is elérhető."
        }
    }

    func toggle() {
        guard let player, isReady else { return }
        if isPlaying {
            player.pause()
            elapsed = player.currentTime
            timer?.invalidate()
            timer = nil
            isPlaying = false
        } else {
            if elapsed >= duration { player.currentTime = 0 }
            guard player.play() else {
                error = "A lejátszás nem indítható. Próbáld újra."
                return
            }
            error = nil
            isPlaying = true
            timer?.invalidate()
            timer = Timer.scheduledTimer(withTimeInterval: 0.2, repeats: true) { [weak self] _ in
                Task { @MainActor [weak self] in
                    guard let self, let audio = self.player else { return }
                    self.elapsed = audio.currentTime
                }
            }
        }
    }

    func stop() {
        timer?.invalidate()
        timer = nil
        player?.stop()
        player?.currentTime = 0
        elapsed = 0
        isPlaying = false
    }

    func seek(to time: TimeInterval) {
        guard let player else { return }
        let position = min(max(0, time), duration)
        player.currentTime = position
        elapsed = position
    }

    func clear() {
        stop()
        player = nil
        isReady = false
        duration = 0
        error = nil
    }

    nonisolated func audioPlayerDidFinishPlaying(_ player: AVAudioPlayer, successfully flag: Bool) {
        let finishedPlayer = ObjectIdentifier(player)
        Task { @MainActor [weak self] in
            guard let self, let current = self.player,
                  ObjectIdentifier(current) == finishedPlayer, !current.isPlaying else { return }
            self.timer?.invalidate()
            self.timer = nil
            self.isPlaying = false
            self.elapsed = self.duration
            if !flag { self.error = "A lejátszás megszakadt." }
        }
    }
}

struct PlaybackControls: View {
    @ObservedObject var player: AudioPlayback

    private func clock(_ time: TimeInterval) -> String {
        let seconds = max(0, Int(time))
        return String(format: "%d:%02d", seconds / 60, seconds % 60)
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("A kész MP3 meghallgatása").font(.headline)
            HStack {
                Button(player.isPlaying ? "Szünet" : "Lejátszás", systemImage: player.isPlaying ? "pause.fill" : "play.fill") {
                    player.toggle()
                }
                .disabled(!player.isReady)
                .accessibilityIdentifier("playPause")
                Button("Leállítás", systemImage: "stop.fill") { player.stop() }
                    .disabled(!player.isReady)
                    .accessibilityIdentifier("stopPlayback")
                Text(player.isPlaying ? "Lejátszás folyamatban" : (player.elapsed >= player.duration && player.duration > 0 ? "Lejátszás vége" : (player.elapsed > 0 ? "Szünetel" : "Leállítva")))
                    .foregroundStyle(.secondary)
                Spacer()
                Image(systemName: "speaker.wave.2")
                Slider(value: $player.volume, in: 0...1)
                    .frame(width: 100)
                    .accessibilityLabel("Lejátszás hangereje")
            }
            HStack {
                Text(clock(player.elapsed)).monospacedDigit()
                Slider(value: Binding(get: { player.elapsed }, set: { player.seek(to: $0) }), in: 0...max(player.duration, 0.1))
                    .disabled(!player.isReady)
                    .accessibilityLabel("Lejátszási pozíció")
                Text(clock(player.duration)).monospacedDigit()
            }
            .font(.caption)
            if let error = player.error { Text(error).foregroundStyle(.red) }
        }
        .padding(14)
        .background(.quaternary.opacity(0.3), in: RoundedRectangle(cornerRadius: 10))
    }
}
