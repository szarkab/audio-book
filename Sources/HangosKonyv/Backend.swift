import Foundation

struct WorkerEvent: Decodable, Sendable {
    let state: String
    let text: String?
    let digest: String?
    let output: String?
    let message: String?
    let completedCharacters: Int?
    let totalCharacters: Int?
}

struct WorkerFailure: LocalizedError {
    let message: String
    var errorDescription: String? { message }
}

struct Backend: Sendable {
    // Development launch only. The standalone bundle is a later ticket.
    let projectRoot: URL = ProcessInfo.processInfo.environment["AUDIOBOOK_PROJECT_ROOT"]
        .map { URL(fileURLWithPath: $0) }
        ?? URL(fileURLWithPath: #filePath)
            .deletingLastPathComponent().deletingLastPathComponent().deletingLastPathComponent()

    func run(
        arguments: [String],
        onEvent: @escaping @MainActor @Sendable (WorkerEvent) -> Void
    ) async throws {
        let root = projectRoot
        try await Task.detached(priority: .userInitiated) {
            let process = Process()
            process.executableURL = root.appendingPathComponent(".venv/bin/python").resolvingSymlinksInPath()
            process.arguments = ["-u", "-m", "audiobook"] + arguments
            process.currentDirectoryURL = root
            var environment = ProcessInfo.processInfo.environment
            environment["PATH"] = "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"
            environment["PYTHONUNBUFFERED"] = "1"
            environment["PYTHONPATH"] = root.path + ":" + root.appendingPathComponent(".venv/lib/python3.12/site-packages").path
            environment["HF_HUB_OFFLINE"] = "1"
            environment["TRANSFORMERS_OFFLINE"] = "1"
            environment["HF_HUB_DISABLE_TELEMETRY"] = "1"
            process.environment = environment
            let pipe = Pipe()
            process.standardOutput = pipe
            let logs = root.appendingPathComponent(".local/logs")
            try FileManager.default.createDirectory(at: logs, withIntermediateDirectories: true)
            let logURL = logs.appendingPathComponent("worker-\(UUID().uuidString).log")
            FileManager.default.createFile(atPath: logURL.path, contents: nil)
            let log = try FileHandle(forWritingTo: logURL)
            defer { try? log.close() }
            process.standardError = log
            do {
                try process.run()
            } catch {
                throw WorkerFailure(message: "A helyi futtatókörnyezet nem indítható. Ellenőrizd a fejlesztői telepítést.")
            }
            var pending = Data()
            var terminalEvent = false
            var failure: String?
            let decoder = JSONDecoder()
            decoder.keyDecodingStrategy = .convertFromSnakeCase
            while true {
                let data = pipe.fileHandleForReading.availableData
                if data.isEmpty { break }
                pending.append(data)
                while let newline = pending.firstIndex(of: 10) {
                    let line = pending.prefix(upTo: newline)
                    pending.removeSubrange(...newline)
                    guard !line.isEmpty else { continue }
                    guard let event = try? decoder.decode(WorkerEvent.self, from: Data(line)) else {
                        process.terminate()
                        process.waitUntilExit()
                        throw WorkerFailure(message: "Nem olvasható a feladat állapota. Próbáld újra.")
                    }
                    if event.state == "ready" || event.state == "completed" { terminalEvent = true }
                    if event.state == "failed" { failure = event.message ?? "A generálás nem sikerült." }
                    await onEvent(event)
                }
            }
            process.waitUntilExit()
            if let failure { throw WorkerFailure(message: failure) }
            guard process.terminationStatus == 0, terminalEvent else {
                throw WorkerFailure(message: "A helyi feladat váratlanul leállt. Ellenőrizd a szabad memóriát és a munkanaplót.")
            }
        }.value
    }
}
