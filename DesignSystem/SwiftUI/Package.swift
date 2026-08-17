// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "UzumeDesignSystem",
    platforms: [.macOS(.v14)],
    products: [
        .library(name: "UzumeDesignSystem", targets: ["UzumeDesignSystem"])
    ],
    targets: [
        .target(name: "UzumeDesignSystem"),
        .testTarget(name: "UzumeDesignSystemTests", dependencies: ["UzumeDesignSystem"])
    ]
)
