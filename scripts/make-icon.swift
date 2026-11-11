import AppKit
import Foundation

// Vector source for the book-and-sound mark. Raster outputs are reproducible.
let destination = URL(fileURLWithPath: CommandLine.arguments[1])
let iconset = destination.appendingPathComponent("AppIcon.iconset")
try FileManager.default.createDirectory(at: iconset, withIntermediateDirectories: true)

func drawMark() {
    let tile = NSBezierPath(roundedRect: NSRect(x: 52, y: 52, width: 920, height: 920), xRadius: 205, yRadius: 205)
    NSGradient(starting: NSColor(srgbRed: 0.09, green: 0.15, blue: 0.28, alpha: 1),
               ending: NSColor(srgbRed: 0.18, green: 0.37, blue: 0.63, alpha: 1))!.draw(in: tile, angle: 45)
    let left = NSBezierPath()
    left.move(to: NSPoint(x: 210, y: 310))
    left.line(to: NSPoint(x: 210, y: 700))
    left.curve(to: NSPoint(x: 504, y: 654), controlPoint1: NSPoint(x: 310, y: 747), controlPoint2: NSPoint(x: 430, y: 718))
    left.line(to: NSPoint(x: 504, y: 274))
    left.curve(to: NSPoint(x: 210, y: 310), controlPoint1: NSPoint(x: 420, y: 338), controlPoint2: NSPoint(x: 300, y: 352))
    left.close()
    NSColor(srgbRed: 0.99, green: 0.97, blue: 0.90, alpha: 1).setFill()
    left.fill()
    let right = left.copy() as! NSBezierPath
    var mirror = AffineTransform()
    mirror.translate(x: 1024, y: 0)
    mirror.scale(x: -1, y: 1)
    right.transform(using: mirror)
    NSColor(srgbRed: 0.88, green: 0.93, blue: 0.98, alpha: 1).setFill()
    right.fill()
    NSColor(srgbRed: 0.87, green: 0.62, blue: 0.22, alpha: 1).setStroke()
    for (index, height) in [80.0, 150.0, 230.0, 150.0, 80.0].enumerated() {
        let line = NSBezierPath()
        line.lineWidth = 27
        line.lineCapStyle = .round
        let x = 416.0 + Double(index) * 48
        line.move(to: NSPoint(x: x, y: 492 - height / 2))
        line.line(to: NSPoint(x: x, y: 492 + height / 2))
        line.stroke()
    }
}

for size in [16, 32, 64, 128, 256, 512, 1024] {
    let bitmap = NSBitmapImageRep(bitmapDataPlanes: nil, pixelsWide: size, pixelsHigh: size,
                                  bitsPerSample: 8, samplesPerPixel: 4, hasAlpha: true,
                                  isPlanar: false, colorSpaceName: .deviceRGB, bytesPerRow: 0, bitsPerPixel: 0)!
    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: bitmap)
    let scale = NSAffineTransform()
    scale.scale(by: CGFloat(size) / 1024)
    scale.concat()
    drawMark()
    NSGraphicsContext.restoreGraphicsState()
    let png = bitmap.representation(using: .png, properties: [:])!
    if [16, 32, 128, 256, 512].contains(size) { try png.write(to: iconset.appendingPathComponent("icon_\(size)x\(size).png")) }
    if [32, 64, 256, 512, 1024].contains(size) { try png.write(to: iconset.appendingPathComponent("icon_\(size/2)x\(size/2)@2x.png")) }
    if size == 1024 { try png.write(to: destination.appendingPathComponent("AppIcon.png")) }
}
