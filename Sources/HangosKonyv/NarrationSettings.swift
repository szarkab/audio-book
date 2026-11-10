import Foundation
import SwiftUI

struct NarrationSettings: Equatable, Sendable {
    var tempo = 1.0
    var voiceVariation = 0.5
    var rhythmVariation = 0.333
    var outputVolume = 1.0
    var normalizeAudio = true
    var sentenceSilence = 0.0

    var workerArguments: [String] {
        ["--length-scale", String(1.0 / tempo),
         "--noise-scale", String(voiceVariation),
         "--noise-w-scale", String(rhythmVariation),
         "--volume", String(outputVolume),
         normalizeAudio ? "--normalize-audio" : "--no-normalize-audio",
         "--sentence-silence", String(sentenceSilence)]
    }
}

struct NarrationSettingsView: View {
    @Binding var settings: NarrationSettings
    let busy: Bool
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        VStack(alignment: .leading, spacing: 18) {
            Text("Felolvasás beállításai").font(.title2.bold())
            Text("A következő MP3 ezekkel az értékekkel készül. Az alapértékek a korábban elfogadott Imre-hangot adják.")
                .font(.callout).foregroundStyle(.secondary)
            VStack(spacing: 16) {
                SettingsSlider(title: "Tempó", value: $settings.tempo, range: 0.5...2.0, step: 0.05,
                               suffix: "×", explanation: "1× az elfogadott tempó. Kisebb érték lassabb beszédet ad.", identifier: "narrationTempo")
                SettingsSlider(title: "Ritmus változatossága", value: $settings.rhythmVariation,
                               range: 0...1, step: 0.001, precision: 3,
                               explanation: "A beszédhangok hosszának változatosságát befolyásolja.", identifier: "narrationRhythm")
                SettingsSlider(title: "Hang változatossága", value: $settings.voiceVariation,
                               range: 0...1, step: 0.01,
                               explanation: "A hangképzés változatosságát befolyásolja, nem háttérzajt ad hozzá.", identifier: "narrationVariation")
                SettingsSlider(title: "MP3 kimeneti hangereje", value: $settings.outputVolume,
                               range: 0.1...2.0, step: 0.05, suffix: "×",
                               explanation: "A mentett hangot módosítja; a lejátszó hangerejétől független.", identifier: "narrationVolume")
                Toggle("Hangerő-normalizálás", isOn: $settings.normalizeAudio)
                    .accessibilityIdentifier("narrationNormalize")
                    .help("Kiegyenlíti a hangrészek szintjét. Kikapcsolva a modell eredeti hangereje marad, kimeneti csúcskorláttal.")
                SettingsSlider(title: "Extra mondatszünet", value: $settings.sentenceSilence,
                               range: 0...1.5, step: 0.05, suffix: " s",
                               explanation: "Ennyi csend kerül a mondatok közé. 0 s: nincs hozzáadott szünet.", identifier: "narrationSilence")
            }
            .disabled(busy)
            Text("A választás az alkalmazás bezárásáig marad meg. A hangsúlyozáshoz nincs külön kapcsoló.")
                .font(.caption).foregroundStyle(.secondary)
            HStack {
                Button("Elfogadott alapértékek visszaállítása") { settings = NarrationSettings() }
                    .disabled(busy).accessibilityIdentifier("resetNarrationSettings")
                Spacer()
                Button("Kész") { dismiss() }.keyboardShortcut(.defaultAction)
            }
        }
        .padding(24)
        .frame(width: 580)
    }
}

private struct SettingsSlider: View {
    let title: String
    @Binding var value: Double
    let range: ClosedRange<Double>
    let step: Double
    var precision = 2
    var suffix = ""
    let explanation: String
    let identifier: String

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            HStack {
                Text(title).font(.headline)
                Spacer()
                Text(value.formatted(.number.precision(.fractionLength(precision)).locale(Locale(identifier: "hu_HU"))) + suffix)
                    .monospacedDigit()
            }
            Slider(value: Binding(
                get: { value },
                set: { value = min(range.upperBound, max(range.lowerBound, ($0 / step).rounded() * step)) }
            ), in: range)
                .accessibilityLabel(title).accessibilityIdentifier(identifier)
            Text(explanation).font(.caption).foregroundStyle(.secondary)
        }
    }
}
