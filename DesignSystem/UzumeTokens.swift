import AppKit
import SwiftUI

/// Migration reference for the macOS application.
/// Production source lives in `DesignSystem/SwiftUI/Sources/UzumeDesignSystem/UzumeTokens.swift`.
enum UzumeColor {
    static let canvas = Color(nsColor: .windowBackgroundColor)
    static let surface = Color(nsColor: .controlBackgroundColor)
    static let surfaceRaised = Color(nsColor: .underPageBackgroundColor)
    static let textPrimary = Color(nsColor: .labelColor)
    static let textSecondary = Color(nsColor: .secondaryLabelColor)
    static let textTertiary = Color(nsColor: .tertiaryLabelColor)
    static let line = Color(nsColor: .separatorColor)
    static let accent = Color(nsColor: NSColor(name: nil) { appearance in
        appearance.bestMatch(from: [.darkAqua, .aqua]) == .darkAqua
            ? NSColor(red: 0.498, green: 0.416, blue: 1.000, alpha: 1)
            : NSColor(red: 0.404, green: 0.325, blue: 0.843, alpha: 1)
    })
    static let success = Color(nsColor: .systemGreen)
    static let warning = Color(nsColor: .systemYellow)
    static let danger = Color(nsColor: .systemRed)
    static let information = Color(nsColor: .systemBlue)
    static let openingViolet = Color(red: 0.498, green: 0.416, blue: 1.000)
    static let openingCyan = Color(red: 0.216, green: 0.839, blue: 0.753)
    static let openingEmber = Color(red: 1.000, green: 0.420, blue: 0.290)
}

enum UzumeSpacing {
    static let x1: CGFloat = 4
    static let x2: CGFloat = 8
    static let x3: CGFloat = 12
    static let x4: CGFloat = 16
    static let x6: CGFloat = 24
    static let x8: CGFloat = 32
    static let x12: CGFloat = 48
}

enum UzumeRadius {
    static let compact: CGFloat = 6
    static let standard: CGFloat = 10
    static let prominent: CGFloat = 14
}

enum UzumeMotion {
    static let immediate = Animation.easeOut(duration: 0.12)
    static let standard = Animation.easeOut(duration: 0.24)
    static let deliberate = Animation.timingCurve(0.22, 1, 0.36, 1, duration: 0.48)
}

extension View {
    /// Applies Uzume's display voice only to brand moments, never dense controls.
    func uzumeDisplay(size: CGFloat) -> some View {
        font(.custom("Alumni Sans", size: size).weight(.semibold))
            .tracking(-0.02 * size)
    }
}
