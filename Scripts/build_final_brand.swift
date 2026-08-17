import AppKit
import CoreText
import Foundation

let root = URL(fileURLWithPath: FileManager.default.currentDirectoryPath)
let fontURL = root.appendingPathComponent("brand/fonts/AlumniSans.ttf") as CFURL
var fontError: Unmanaged<CFError>?
guard CTFontManagerRegisterFontsForURL(fontURL, .process, &fontError) else {
    fatalError("Unable to register Alumni Sans: \(String(describing: fontError))")
}

func xml(_ value: String) -> String {
    value.replacingOccurrences(of: "&", with: "&amp;")
        .replacingOccurrences(of: "<", with: "&lt;")
        .replacingOccurrences(of: ">", with: "&gt;")
        .replacingOccurrences(of: "\"", with: "&quot;")
}

func svgPath(_ path: CGPath, baseline: CGFloat) -> String {
    var commands: [String] = []
    path.applyWithBlock { pointer in
        let element = pointer.pointee
        func point(_ p: CGPoint) -> String { String(format: "%.2f %.2f", p.x, baseline - p.y) }
        switch element.type {
        case .moveToPoint: commands.append("M\(point(element.points[0]))")
        case .addLineToPoint: commands.append("L\(point(element.points[0]))")
        case .addQuadCurveToPoint:
            commands.append("Q\(point(element.points[0])) \(point(element.points[1]))")
        case .addCurveToPoint:
            commands.append("C\(point(element.points[0])) \(point(element.points[1])) \(point(element.points[2]))")
        case .closeSubpath: commands.append("Z")
        @unknown default: break
        }
    }
    return commands.joined(separator: " ")
}

func outlinedText(_ string: String, size: CGFloat, weight: CGFloat, tracking: CGFloat) -> (paths: [String], width: CGFloat) {
    let base = CTFontCreateWithName("AlumniSansRoman-Regular" as CFString, size, nil)
    let descriptor = CTFontDescriptorCreateCopyWithVariation(
        CTFontCopyFontDescriptor(base),
        NSNumber(value: 2003265652),
        CGFloat(weight)
    )
    let weighted = CTFontCreateWithFontDescriptor(descriptor, size, nil)
    let attributes: [NSAttributedString.Key: Any] = [
        NSAttributedString.Key(kCTFontAttributeName as String): weighted,
        NSAttributedString.Key(kCTKernAttributeName as String): tracking,
    ]
    let line = CTLineCreateWithAttributedString(NSAttributedString(string: string, attributes: attributes))
    let runs = CTLineGetGlyphRuns(line) as! [CTRun]
    var result: [String] = []
    for run in runs {
        let count = CTRunGetGlyphCount(run)
        var glyphs = Array(repeating: CGGlyph(), count: count)
        var positions = Array(repeating: CGPoint.zero, count: count)
        CTRunGetGlyphs(run, CFRange(location: 0, length: 0), &glyphs)
        CTRunGetPositions(run, CFRange(location: 0, length: 0), &positions)
        for index in 0..<count {
            guard let glyphPath = CTFontCreatePathForGlyph(weighted, glyphs[index], nil) else { continue }
            var transform = CGAffineTransform(translationX: positions[index].x, y: positions[index].y)
            if let moved = glyphPath.copy(using: &transform) {
                result.append(svgPath(moved, baseline: size * 0.9))
            }
        }
    }
    return (result, CGFloat(CTLineGetTypographicBounds(line, nil, nil, nil)))
}

func writeWordmark() throws {
    let output = root.appendingPathComponent("brand/wordmark")
    try FileManager.default.createDirectory(at: output, withIntermediateDirectories: true)
    let word = outlinedText("Uzume", size: 160, weight: 600, tracking: -2.4)
    let width = ceil(word.width + 8)
    let paths = word.paths.map { "    <path d=\"\($0)\"/>" }.joined(separator: "\n")
    let primary = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 \(Int(width)) 160" role="img" aria-labelledby="title desc">
      <title id="title">Uzume wordmark</title>
      <desc id="desc">Uzume set in outlined Alumni Sans SemiBold letterforms.</desc>
      <g fill="#F4F6F1">
    \(paths)
      </g>
    </svg>
    """
    try primary.write(to: output.appendingPathComponent("Uzume.svg"), atomically: true, encoding: .utf8)

    let pronunciation = outlinedText("OO-ZOO-MEH", size: 26, weight: 600, tracking: 2.5)
    let pronPaths = pronunciation.paths.map { "    <path d=\"\($0)\"/>" }.joined(separator: "\n")
    let lockupHeight = 205
    let lockupWidth = Int(max(width, pronunciation.width + 8))
    let lockup = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 \(lockupWidth) \(lockupHeight)" role="img" aria-labelledby="title desc">
      <title id="title">Uzume wordmark with pronunciation</title>
      <desc id="desc">The Uzume wordmark above the pronunciation oo-ZOO-meh.</desc>
      <g fill="#F4F6F1">
    \(paths)
      </g>
      <g fill="#C5C9C3" transform="translate(2 164)">
    \(pronPaths)
      </g>
    </svg>
    """
    try lockup.write(to: output.appendingPathComponent("Uzume-pronunciation.svg"), atomically: true, encoding: .utf8)
}

func resize(_ source: NSImage, pixels: Int, destination: URL) throws {
    guard let bitmap = NSBitmapImageRep(
        bitmapDataPlanes: nil,
        pixelsWide: pixels,
        pixelsHigh: pixels,
        bitsPerSample: 8,
        samplesPerPixel: 4,
        hasAlpha: true,
        isPlanar: false,
        colorSpaceName: .deviceRGB,
        bytesPerRow: 0,
        bitsPerPixel: 0
    ) else { fatalError("Unable to allocate bitmap") }
    bitmap.size = NSSize(width: pixels, height: pixels)
    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.current = NSGraphicsContext(bitmapImageRep: bitmap)
    NSGraphicsContext.current?.imageInterpolation = .high
    source.draw(in: NSRect(x: 0, y: 0, width: pixels, height: pixels), from: .zero, operation: .copy, fraction: 1)
    NSGraphicsContext.restoreGraphicsState()
    guard let data = bitmap.representation(using: .png, properties: [:]) else { fatalError("Unable to encode PNG") }
    try data.write(to: destination)
}

func writeIconset() throws {
    let masterURL = root.appendingPathComponent("brand/icon-candidates/first-opening/icon-first-opening-v1-1024.png")
    guard let source = NSImage(contentsOf: masterURL) else { fatalError("Missing First Opening master") }
    let iconDirectory = root.appendingPathComponent("brand/icon")
    let iconset = iconDirectory.appendingPathComponent("Uzume.iconset")
    try FileManager.default.createDirectory(at: iconDirectory, withIntermediateDirectories: true)
    try FileManager.default.createDirectory(at: iconset, withIntermediateDirectories: true)
    try FileManager.default.copyItemReplacing(at: masterURL, to: iconDirectory.appendingPathComponent("Uzume-1024.png"))
    let exports = [
        (16, "icon_16x16.png"), (32, "icon_16x16@2x.png"),
        (32, "icon_32x32.png"), (64, "icon_32x32@2x.png"),
        (128, "icon_128x128.png"), (256, "icon_128x128@2x.png"),
        (256, "icon_256x256.png"), (512, "icon_256x256@2x.png"),
        (512, "icon_512x512.png"), (1024, "icon_512x512@2x.png"),
    ]
    for (pixels, name) in exports { try resize(source, pixels: pixels, destination: iconset.appendingPathComponent(name)) }

    // macOS 26's iconutil currently rejects otherwise complete legacy iconsets.
    // Package the same PNG representations directly in the documented ICNS
    // chunk container so RN.1 receives both current asset inputs and an .icns.
    let chunks: [(String, String)] = [
        ("icp4", "icon_16x16.png"),
        ("icp5", "icon_32x32.png"),
        ("icp6", "icon_32x32@2x.png"),
        ("ic07", "icon_128x128.png"),
        ("ic08", "icon_256x256.png"),
        ("ic09", "icon_512x512.png"),
        ("ic10", "icon_512x512@2x.png"),
    ]
    var payload = Data()
    for (type, filename) in chunks {
        let png = try Data(contentsOf: iconset.appendingPathComponent(filename))
        payload.append(type.data(using: .ascii)!)
        var length = UInt32(png.count + 8).bigEndian
        withUnsafeBytes(of: &length) { payload.append(contentsOf: $0) }
        payload.append(png)
    }
    var icns = Data("icns".utf8)
    var totalLength = UInt32(payload.count + 8).bigEndian
    withUnsafeBytes(of: &totalLength) { icns.append(contentsOf: $0) }
    icns.append(payload)
    try icns.write(to: iconDirectory.appendingPathComponent("Uzume.icns"))
}

func writeFavicons() throws {
    let sourceURL = root.appendingPathComponent("brand/icon-candidates/first-opening/favicon-study/favicon-crop-v4-512.png")
    guard let source = NSImage(contentsOf: sourceURL) else { fatalError("Missing favicon crop") }
    let output = root.appendingPathComponent("brand/favicon")
    try FileManager.default.createDirectory(at: output, withIntermediateDirectories: true)
    for size in [16, 32, 64, 180, 512] { try resize(source, pixels: size, destination: output.appendingPathComponent("favicon-\(size).png")) }
    let png = try Data(contentsOf: output.appendingPathComponent("favicon-512.png"))
    let svg = """
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" role="img" aria-labelledby="title desc">
      <title id="title">Uzume First Opening favicon</title>
      <desc id="desc">An art-directed crop of the First Opening artwork for small browser contexts.</desc>
      <image width="512" height="512" href="data:image/png;base64,\(png.base64EncodedString())"/>
    </svg>
    """
    try svg.write(to: output.appendingPathComponent("favicon.svg"), atomically: true, encoding: .utf8)
}

extension FileManager {
    func copyItemReplacing(at source: URL, to destination: URL) throws {
        if fileExists(atPath: destination.path) { try removeItem(at: destination) }
        try copyItem(at: source, to: destination)
    }
}

try writeWordmark()
try writeIconset()
try writeFavicons()
print("Built outlined wordmarks, Uzume.iconset, final icon master, and favicon derivatives.")
