import AppKit
import SwiftUI
import UniformTypeIdentifiers

@MainActor
final class GenerationModel: ObservableObject {
    static let shared = GenerationModel()
    @Published var source: URL?
    @Published var preview = ""
    @Published var digest = ""
    @Published var output: URL?
    @Published var busy = false
    @Published var progress: Double?
    @Published var status = "Válassz egy magyar TXT-fájlt."
    @Published var error: String?
    @Published var settings = NarrationSettings()
    @Published var modelState = "model_checking"
    @Published var modelMessage = "A narrátor ellenőrzése…"
    @Published var modelCompletedBytes = 0
    @Published var modelTotalBytes = 0
    @Published var modelDiskBytes = 0
    @Published var modelSource: URL?
    @Published var modelLicenseSource: URL?
    var modelReady: Bool { modelState == "model_ready" }
    let playback = AudioPlayback()
    private let backend = Backend()

    func refreshModel() async {
        guard !busy else { return }
        busy = true
        defer { busy = false }
        do {
            try await backend.run(arguments: ["model-status"]) { [self] event in updateModel(event) }
        } catch {
            modelState = "model_failed"
            modelMessage = "A narrátor ellenőrzése sikertelen."
            show(error)
        }
    }

    func downloadModel() {
        guard !busy else { return }
        busy = true
        error = nil
        modelState = "model_downloading"
        modelMessage = "Az Imre-hang letöltése…"
        modelCompletedBytes = 0
        status = "A modell beszerzése folyamatban van…"
        Task {
            defer { busy = false }
            do {
                try await backend.run(arguments: ["download-model"]) { [self] event in updateModel(event) }
                status = source == nil ? "Válassz egy magyar TXT-fájlt." : "A szöveg készen áll a felolvasásra."
            } catch {
                modelState = "model_failed"
                modelMessage = "A letöltés nem sikerült. Újrapróbálható."
                show(error)
            }
        }
    }

    private func updateModel(_ event: WorkerEvent) {
        guard event.state.hasPrefix("model_") else { return }
        modelState = event.state
        modelCompletedBytes = event.completedBytes ?? 0
        modelTotalBytes = event.totalBytes ?? 0
        modelDiskBytes = event.diskBytes ?? 0
        modelSource = event.source.flatMap(URL.init(string:))
        modelLicenseSource = event.licenseSource.flatMap(URL.init(string:))
        switch event.state {
        case "model_ready": modelMessage = "Imre-hang: használatra kész · Offline működés"
        case "model_missing": modelMessage = "Az Imre-hang még nincs letöltve."
        case "model_damaged": modelMessage = "Az Imre-hang hiányos vagy sérült. Újra letölthető."
        case "model_downloading": modelMessage = "Az Imre-hang letöltése…"
        default: break
        }
    }

    func selectSource() {
        let panel = NSOpenPanel()
        panel.allowedContentTypes = [UTType(filenameExtension: "txt") ?? .plainText]
        panel.allowsMultipleSelection = false
        panel.canChooseDirectories = false
        guard panel.runModal() == .OK, let url = panel.url else { return }
        playback.clear()
        source = nil
        preview = ""
        digest = ""
        output = nil
        error = nil
        progress = nil
        busy = true
        status = "A szöveg betöltése…"
        Task {
            defer { busy = false }
            do {
                try await backend.run(arguments: ["preview", url.path]) { [self] event in
                    if event.state == "ready", let text = event.text, let hash = event.digest {
                        source = url
                        preview = text
                        digest = hash
                        status = "A szöveg készen áll a felolvasásra."
                    }
                }
            } catch { show(error) }
        }
    }

    func generate() {
        guard let source, !busy, modelReady else { return }
        playback.stop()
        let panel = NSSavePanel()
        panel.allowedContentTypes = [.mp3]
        panel.nameFieldStringValue = source.deletingPathExtension().lastPathComponent + "-hang.mp3"
        panel.canCreateDirectories = true
        panel.message = "Válassz új fájlnevet. Meglévő hanganyagot nem írunk felül."
        guard panel.runModal() == .OK, let target = panel.url else { return }
        error = nil
        output = nil
        progress = nil
        busy = true
        status = "A felolvasás indítása…"
        let expectedDigest = digest
        let jobSettings = settings
        Task {
            defer { busy = false }
            do {
                try await backend.run(arguments: [
                    "generate", source.path, "--output", target.path, "--expected-digest", expectedDigest
                ] + jobSettings.workerArguments) { [self] event in
                    if let message = event.message { status = message }
                    if let completed = event.completedCharacters, let total = event.totalCharacters, total > 0 {
                        progress = min(1, max(0, Double(completed) / Double(total)))
                    }
                    if event.state == "completed", let path = event.output {
                        let url = URL(fileURLWithPath: path)
                        output = url
                        playback.load(url)
                    }
                }
            } catch { show(error) }
        }
    }

    private func show(_ failure: Error) {
        error = failure.localizedDescription
        status = "A feladat nem sikerült."
    }
}

@MainActor
final class AppDelegate: NSObject, NSApplicationDelegate {
    func applicationDidFinishLaunching(_ notification: Notification) {
        NSApp.setActivationPolicy(.regular)
        NSApp.activate(ignoringOtherApps: true)
    }

    func applicationShouldTerminate(_ sender: NSApplication) -> NSApplication.TerminateReply {
        guard GenerationModel.shared.busy else { return .terminateNow }
        let alert = NSAlert()
        alert.messageText = "A feladat még folyamatban van."
        alert.informativeText = "Várd meg, amíg elkészül az MP3, és utána zárd be az alkalmazást."
        alert.runModal()
        return .terminateCancel
    }

    func applicationShouldTerminateAfterLastWindowClosed(_ sender: NSApplication) -> Bool { true }
}

struct ContentView: View {
    @ObservedObject var model: GenerationModel
    @State private var showingSettings = false

    var body: some View {
        VStack(alignment: .leading, spacing: 20) {
            HStack(alignment: .top) {
                VStack(alignment: .leading, spacing: 6) {
                    Text("Hangoskönyv").font(.largeTitle.bold())
                    Text("Magyar szövegből nyugodt, férfihangos felolvasás.")
                        .foregroundStyle(.secondary)
                }
                Spacer()
                Label("Helyben fut", systemImage: "desktopcomputer")
                    .font(.callout).foregroundStyle(.secondary)
            }
            ModelDownloadView(model: model)
            HStack {
                Button("TXT-fájl kiválasztása…", systemImage: "doc.badge.plus") { model.selectSource() }
                    .disabled(model.busy)
                    .accessibilityIdentifier("selectSource")
                Text(model.source?.lastPathComponent ?? "Nincs kiválasztott fájl")
                    .foregroundStyle(.secondary).lineLimit(1).truncationMode(.middle)
                Spacer()
            }
            HStack {
                Button("Felolvasás beállításai…", systemImage: "slider.horizontal.3") { showingSettings = true }
                    .disabled(model.busy).accessibilityIdentifier("narrationSettings")
                Text(model.settings == NarrationSettings() ? "Elfogadott alapértékek" : "Egyéni beállítások")
                    .font(.caption).foregroundStyle(.secondary)
                Spacer()
            }
            HStack {
                Text("Felolvasandó szöveg").font(.headline)
                Spacer()
                Text("\(model.preview.count.formatted()) karakter").font(.caption).foregroundStyle(.secondary)
            }
            ScrollView {
                Text(model.preview.isEmpty ? "A kiválasztott szöveg itt jelenik meg." : model.preview)
                    .font(.system(size: 16)).lineSpacing(6).textSelection(.enabled)
                    .foregroundStyle(model.preview.isEmpty ? .secondary : .primary)
                    .frame(maxWidth: .infinity, alignment: .topLeading)
                    .padding(16)
            }
            .frame(minHeight: model.output == nil ? 220 : 140)
            .background(.background, in: RoundedRectangle(cornerRadius: 12))
            .overlay(RoundedRectangle(cornerRadius: 12).stroke(.quaternary))
            if let error = model.error {
                Label(error, systemImage: "exclamationmark.triangle")
                    .foregroundStyle(.red).textSelection(.enabled)
            }
            if model.output != nil { PlaybackControls(player: model.playback) }
            if model.busy, let progress = model.progress {
                VStack(alignment: .leading, spacing: 5) {
                    ProgressView(value: progress)
                    Text("Feldolgozott szöveg: \(Int(progress * 100))%")
                        .font(.caption).foregroundStyle(.secondary)
                }
            }
            HStack(spacing: 12) {
                if model.busy { ProgressView().controlSize(.small) }
                Text(model.status).foregroundStyle(.secondary)
                Spacer()
                if let output = model.output {
                    Button("Mutasd a Finderben") { NSWorkspace.shared.activateFileViewerSelecting([output]) }
                }
                Button("MP3 készítése", systemImage: "waveform") { model.generate() }
                    .buttonStyle(.borderedProminent)
                    .disabled(model.source == nil || model.busy || !model.modelReady)
                    .accessibilityIdentifier("generate")
            }
            Text("Piper Imre · Magyar férfihang · MP3")
                .font(.caption).foregroundStyle(.secondary)
        }
        .padding(28)
        .frame(minWidth: 760, minHeight: 800)
        .task { await model.refreshModel() }
        .sheet(isPresented: $showingSettings) {
            NarrationSettingsView(settings: $model.settings, busy: model.busy)
        }
    }
}

@main
struct HangosKonyvApp: App {
    @NSApplicationDelegateAdaptor(AppDelegate.self) var delegate
    var body: some Scene {
        WindowGroup {
            ContentView(model: GenerationModel.shared)
        }
        .defaultSize(width: 900, height: 880)
        .commands {
            CommandGroup(replacing: .newItem) { }
        }
    }
}
