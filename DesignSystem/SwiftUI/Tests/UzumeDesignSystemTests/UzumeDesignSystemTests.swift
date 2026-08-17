import Testing
@testable import UzumeDesignSystem

@Test func statusAndPreparationVocabulariesAreStable() {
    #expect(UzumeStatusTone.allCases.map(\.rawValue) == ["information", "success", "warning", "error"])
    #expect(UzumePreparationPhase.allCases.map(\.rawValue) == ["Listening", "Separating", "Understanding", "Composing"])
}

@Test func preflightSummaryPreservesProductFacts() {
    let summary = UzumePreflightSummary(audio: "System audio", display: "External display", repertoire: "24 presets", accessibility: "Reduced motion")
    #expect(summary.audio == "System audio")
    #expect(summary.repertoire == "24 presets")
}
