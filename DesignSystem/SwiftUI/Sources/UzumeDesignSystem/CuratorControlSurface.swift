import SwiftUI

public struct CuratorControlSurface: View {
    @Binding private var showsTrackInformation: Bool
    private let endSession: () -> Void

    public init(showsTrackInformation: Binding<Bool>, endSession: @escaping () -> Void) {
        _showsTrackInformation = showsTrackInformation
        self.endSession = endSession
    }

    public var body: some View {
        HStack(spacing: UzumeSpace.x4) {
            Label("Listening", systemImage: "waveform")
                .foregroundStyle(UzumeColor.success)
                .accessibilityLabel("Uzume is listening")
            Spacer()
            Toggle("Track information", isOn: $showsTrackInformation)
                .toggleStyle(.switch)
            Button("End session", role: .destructive, action: endSession)
        }
        .padding(UzumeSpace.x4)
        .background(.regularMaterial, in: RoundedRectangle(cornerRadius: UzumeRadius.standard))
        .uzumeTint()
    }
}
