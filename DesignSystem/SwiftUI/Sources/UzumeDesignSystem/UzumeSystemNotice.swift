import SwiftUI

public enum UzumeStatusTone: String, CaseIterable, Sendable {
    case information, success, warning, error

    public var title: String { rawValue.capitalized }

    var symbolName: String {
        switch self {
        case .information: "info.circle.fill"
        case .success: "checkmark.circle.fill"
        case .warning: "exclamationmark.triangle.fill"
        case .error: "xmark.octagon.fill"
        }
    }

    var color: Color {
        switch self {
        case .information: UzumeColor.information
        case .success: UzumeColor.success
        case .warning: UzumeColor.warning
        case .error: UzumeColor.danger
        }
    }
}

public struct UzumeSystemNotice<Actions: View>: View {
    private let tone: UzumeStatusTone
    private let title: String
    private let message: String
    private let actions: Actions

    public init(
        tone: UzumeStatusTone,
        title: String,
        message: String,
        @ViewBuilder actions: () -> Actions
    ) {
        self.tone = tone
        self.title = title
        self.message = message
        self.actions = actions()
    }

    public var body: some View {
        HStack(alignment: .top, spacing: UzumeSpace.x3) {
            Image(systemName: tone.symbolName)
                .symbolRenderingMode(.palette)
                .foregroundStyle(symbolDetail, tone.color)
                .font(.title2)
                .accessibilityHidden(true)

            VStack(alignment: .leading, spacing: UzumeSpace.x2) {
                Text(title).font(.headline)
                Text(message).foregroundStyle(.secondary).fixedSize(horizontal: false, vertical: true)
                HStack(spacing: UzumeSpace.x2) { actions }
            }
        }
        .padding(UzumeSpace.x4)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(.background.secondary, in: RoundedRectangle(cornerRadius: UzumeRadius.standard))
        .accessibilityElement(children: .contain)
    }

    private var symbolDetail: Color {
        tone == .warning ? .black : .white
    }
}

public extension UzumeSystemNotice where Actions == EmptyView {
    init(tone: UzumeStatusTone, title: String, message: String) {
        self.init(tone: tone, title: title, message: message) { EmptyView() }
    }
}
