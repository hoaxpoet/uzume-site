import SwiftUI

public struct UzumePreflightSummary: Sendable, Equatable {
    public let audio: String
    public let display: String
    public let repertoire: String
    public let accessibility: String

    public init(audio: String, display: String, repertoire: String, accessibility: String) {
        self.audio = audio
        self.display = display
        self.repertoire = repertoire
        self.accessibility = accessibility
    }
}

public struct PerformancePreflight: View {
    private let summary: UzumePreflightSummary
    private let addMusic: () -> Void
    private let openSettings: () -> Void

    public init(summary: UzumePreflightSummary, addMusic: @escaping () -> Void, openSettings: @escaping () -> Void) {
        self.summary = summary
        self.addMusic = addMusic
        self.openSettings = openSettings
    }

    public var body: some View {
        VStack(alignment: .leading, spacing: UzumeSpace.x6) {
            VStack(alignment: .leading, spacing: UzumeSpace.x2) {
                Text("Ready the performance").font(.largeTitle.weight(.semibold))
                Text("Confirm the boundaries. Uzume will choose what happens inside them.")
                    .foregroundStyle(.secondary)
            }

            Grid(alignment: .leading, horizontalSpacing: UzumeSpace.x8, verticalSpacing: UzumeSpace.x3) {
                summaryRow("Audio", summary.audio, symbol: "waveform")
                summaryRow("Display", summary.display, symbol: "display.2")
                summaryRow("Repertoire", summary.repertoire, symbol: "square.grid.2x2")
                summaryRow("Experience", summary.accessibility, symbol: "accessibility")
            }

            HStack {
                Button("Settings", action: openSettings)
                Spacer()
                Button("Add music", action: addMusic).buttonStyle(.borderedProminent)
            }
        }
        .padding(UzumeSpace.x8)
        .uzumeTint()
    }

    private func summaryRow(_ label: String, _ value: String, symbol: String) -> some View {
        GridRow {
            Label(label, systemImage: symbol).foregroundStyle(.secondary)
            Text(value).gridColumnAlignment(.leading)
        }
    }
}
