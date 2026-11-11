import SwiftUI

struct ModelDownloadView: View {
    @ObservedObject var model: GenerationModel

    var body: some View {
        VStack(alignment: .leading, spacing: 7) {
            HStack {
                Label(model.modelMessage, systemImage: model.modelReady ? "checkmark.circle" : "arrow.down.circle")
                    .font(.callout)
                Spacer()
                if !model.modelReady {
                    Button(model.modelState == "model_failed" || model.modelState == "model_damaged"
                           ? "Letöltés újrapróbálása" : "Imre-hang letöltése") { model.downloadModel() }
                        .disabled(model.busy).accessibilityIdentifier("downloadModel")
                }
            }
            if model.modelState == "model_downloading", model.modelTotalBytes > 0 {
                ProgressView(value: Double(model.modelCompletedBytes), total: Double(model.modelTotalBytes))
                Text("\(bytes(model.modelCompletedBytes)) / \(bytes(model.modelTotalBytes))")
                    .font(.caption).monospacedDigit()
            }
            HStack(spacing: 12) {
                if model.modelTotalBytes > 0 {
                    Text("Letöltés: \(bytes(model.modelTotalBytes)) · Szükséges szabad hely: \(bytes(model.modelDiskBytes))")
                }
                Spacer()
                if let source = model.modelSource {
                    Link("Modell eredete", destination: source)
                }
                if let license = model.modelLicenseSource {
                    Link("Adatkészlet: CC0", destination: license)
                }
                Link("Piper: GPL-3.0", destination: URL(string: "https://github.com/OHF-Voice/piper1-gpl/blob/main/COPYING")!)
            }
            .font(.caption).foregroundStyle(.secondary)
        }
        .padding(12)
        .background(AppBrand.accent.opacity(0.09), in: RoundedRectangle(cornerRadius: 10))
    }

    private func bytes(_ count: Int) -> String {
        ByteCountFormatter.string(fromByteCount: Int64(count), countStyle: .file)
    }
}
