import SwiftUI

public enum UzumePreparationPhase: String, CaseIterable, Sendable {
    case listening = "Listening"
    case separating = "Separating"
    case understanding = "Understanding"
    case composing = "Composing"
}

public struct PreparationStage: View {
    private let phase: UzumePreparationPhase
    private let completed: Int
    private let total: Int
    private let timeRemaining: String?
    private let cancel: () -> Void

    public init(phase: UzumePreparationPhase, completed: Int, total: Int, timeRemaining: String? = nil, cancel: @escaping () -> Void) {
        self.phase = phase
        self.completed = completed
        self.total = total
        self.timeRemaining = timeRemaining
        self.cancel = cancel
    }

    public var body: some View {
        ZStack(alignment: .bottomLeading) {
            Color.black
            FirstOpeningField(progress: progress)
                .accessibilityHidden(true)

            VStack(alignment: .leading, spacing: UzumeSpace.x4) {
                Text("Preparing your performance").foregroundStyle(.secondary)
                Text(phase.rawValue).font(.system(size: 48, weight: .semibold, design: .rounded))
                ProgressView(value: progress)
                    .progressViewStyle(.linear)
                    .tint(.white)
                    .accessibilityLabel("Tracks prepared")
                    .accessibilityValue("\(completed) of \(total)")
                HStack {
                    Text("\(completed) of \(total) tracks")
                    if let timeRemaining { Text("· \(timeRemaining)") }
                    Spacer()
                    Button("Cancel", action: cancel).buttonStyle(.plain)
                }
                .foregroundStyle(.secondary)
            }
            .padding(UzumeSpace.x12)
        }
        .foregroundStyle(.white)
        .frame(minWidth: 640, minHeight: 420)
        .clipped()
        .accessibilityElement(children: .contain)
    }

    private var progress: Double {
        guard total > 0 else { return 0 }
        return min(max(Double(completed) / Double(total), 0), 1)
    }
}

private struct FirstOpeningField: View {
    let progress: Double

    var body: some View {
        GeometryReader { proxy in
            UzumeColor.performedLight
                .mask {
                    Path { path in
                        let width = proxy.size.width
                        let height = proxy.size.height
                        let opening = width * (0.07 + 0.18 * progress)
                        path.move(to: CGPoint(x: width * 0.56, y: -20))
                        path.addCurve(to: CGPoint(x: width * 0.48 - opening, y: height * 0.52), control1: CGPoint(x: width * 0.68, y: height * 0.18), control2: CGPoint(x: width * 0.44, y: height * 0.34))
                        path.addCurve(to: CGPoint(x: width * 0.72, y: height + 20), control1: CGPoint(x: width * 0.55, y: height * 0.72), control2: CGPoint(x: width * 0.58 + opening, y: height * 0.84))
                        path.addLine(to: CGPoint(x: width + 20, y: height + 20))
                        path.addLine(to: CGPoint(x: width + 20, y: -20))
                        path.closeSubpath()
                    }
                }
        }
    }
}
