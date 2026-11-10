// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "HangosKonyv",
    platforms: [.macOS(.v14)],
    products: [.executable(name: "HangosKonyv", targets: ["HangosKonyv"])],
    targets: [.executableTarget(name: "HangosKonyv")]
)
