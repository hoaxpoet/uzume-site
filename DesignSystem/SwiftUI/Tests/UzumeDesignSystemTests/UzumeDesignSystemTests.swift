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

@Test func motionDurationsMatchTheCSSTokens() {
    // The values in tokens.css: --duration-immediate/standard/deliberate.
    // DS.6 finding 1 — the app transcribed these because the package did not carry
    // them, and the curve drifted. Pin them so the two surfaces cannot diverge again.
    #expect(UzumeMotion.feedback == 0.12)
    #expect(UzumeMotion.standard == 0.24)
    #expect(UzumeMotion.opening == 0.48)
}
