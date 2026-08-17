import SwiftUI

public struct StreamingHandoff: View {
    private let sourceName: String
    private let isListening: Bool
    private let retry: () -> Void

    public init(sourceName: String, isListening: Bool, retry: @escaping () -> Void) {
        self.sourceName = sourceName
        self.isListening = isListening
        self.retry = retry
    }

    public var body: some View {
        VStack(spacing: UzumeSpace.x4) {
            Image(systemName: isListening ? "waveform.badge.magnifyingglass" : "play.circle")
                .font(.system(size: 36))
                .foregroundStyle(UzumeColor.accent)
            Text("Performance ready").font(.title2.weight(.semibold))
            Text("Start the playlist in \(sourceName). Uzume will begin the moment it hears the music.")
                .multilineTextAlignment(.center)
                .foregroundStyle(.secondary)
                .frame(maxWidth: 420)
            if isListening {
                ProgressView().controlSize(.small).accessibilityLabel("Listening for audio")
            } else {
                Button("Listen again", action: retry).buttonStyle(.borderedProminent)
            }
        }
        .padding(UzumeSpace.x8)
        .uzumeTint()
    }
}
