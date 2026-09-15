import AppKit
import SwiftUI

public enum UzumeColor {
    public static let canvas = Color(nsColor: .windowBackgroundColor)
    public static let surface = Color(nsColor: .controlBackgroundColor)
    public static let textPrimary = Color(nsColor: .labelColor)
    public static let textSecondary = Color(nsColor: .secondaryLabelColor)
    public static let line = Color(nsColor: .separatorColor)
    public static let accent = adaptive(
        light: NSColor(red: 0.404, green: 0.325, blue: 0.843, alpha: 1),
        dark: NSColor(red: 0.498, green: 0.416, blue: 1.000, alpha: 1)
    )
    public static let violet = Color(red: 0.498, green: 0.416, blue: 1.000)
    public static let cyan = Color(red: 0.216, green: 0.839, blue: 0.753)
    public static let gold = Color(red: 0.961, green: 0.784, blue: 0.298)
    public static let ember = Color(red: 1.000, green: 0.420, blue: 0.290)
    public static let success = Color(nsColor: .systemGreen)
    public static let warning = Color(nsColor: .systemYellow)
    public static let danger = Color(nsColor: .systemRed)
    public static let information = Color(nsColor: .systemBlue)

    public static let performedLight = LinearGradient(
        stops: [
            .init(color: violet, location: 0),
            .init(color: cyan, location: 0.38),
            .init(color: gold, location: 0.68),
            .init(color: ember, location: 1)
        ],
        startPoint: .topLeading,
        endPoint: .bottomTrailing
    )

    private static func adaptive(light: NSColor, dark: NSColor) -> Color {
        Color(nsColor: NSColor(name: nil) { appearance in
            appearance.bestMatch(from: [.darkAqua, .aqua]) == .darkAqua ? dark : light
        })
    }
}

public enum UzumeSpace {
    public static let x1: CGFloat = 4
    public static let x2: CGFloat = 8
    public static let x3: CGFloat = 12
    public static let x4: CGFloat = 16
    public static let x6: CGFloat = 24
    public static let x8: CGFloat = 32
    public static let x12: CGFloat = 48
}

public enum UzumeRadius {
    public static let compact: CGFloat = 6
    public static let standard: CGFloat = 10
    public static let prominent: CGFloat = 14
}

/// Mirrors the `--duration-*` and `--ease-out` tokens in `tokens.css`. Published here
/// so the app can consume these rather than transcribe them: DS.6 finding 1 recorded
/// that the design system named three durations and a curve in `DESIGN.md` while
/// neither token file carried them, so `UzumeAppMotion` had to restate the numbers —
/// and the curve then drifted from the site's for months without anything noticing.
public enum UzumeMotion {
    /// `--duration-immediate` — control feedback.
    public static let feedback: Double = 0.12
    /// `--duration-standard` — a standard state change.
    public static let standard: Double = 0.24
    /// `--duration-deliberate` — an authored opening.
    public static let opening: Double = 0.48

    /// Exponential ease-out. SwiftUI has no `easeOutExpo`; this is its usual
    /// cubic-bezier approximation, the same control points as `--ease-out`.
    public static func easeOut(_ duration: Double) -> Animation {
        .timingCurve(0.16, 1, 0.3, 1, duration: duration)
    }

    /// A state change: the ease-out, or under reduced motion a plain crossfade of the
    /// same length. Opacity only either way — callers keep spatial transitions out.
    public static func stateChange(reduceMotion: Bool) -> Animation {
        reduceMotion ? .easeInOut(duration: standard) : easeOut(standard)
    }
}

public extension View {
    func uzumeTint() -> some View { tint(UzumeColor.accent) }
}
