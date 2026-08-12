#!/usr/bin/env python3
"""Render the redirected BRAND.1 app-icon directions from exact geometry."""

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SCALE = 4
SIZE = 1024


def box(values):
    return tuple(round(value * SCALE) for value in values)


def canvas(color):
    image = Image.new("RGBA", (SIZE * SCALE, SIZE * SCALE), (0, 0, 0, 0))
    ImageDraw.Draw(image).rounded_rectangle(box((64, 64, 960, 960)), radius=224 * SCALE, fill=color)
    return image


def bar(image, bounds, radius, color, angle=0):
    if not angle:
        ImageDraw.Draw(image).rounded_rectangle(box(bounds), radius=radius * SCALE, fill=color)
        return
    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).rounded_rectangle(box(bounds), radius=radius * SCALE, fill=color)
    layer = layer.rotate(angle, resample=Image.Resampling.BICUBIC, center=(image.width // 2, image.height // 2))
    image.alpha_composite(layer)


def measure():
    image = canvas("#0B0C10")
    bars = (
        ((174, 452, 266, 734), "#7F6AFF"),
        ((320, 280, 412, 754), "#37D6C0"),
        ((466, 524, 558, 722), "#F5C84C"),
        ((612, 210, 704, 798), "#FF6B4A"),
        ((758, 392, 850, 754), "#F4F6F1"),
    )
    for bounds, color in bars:
        bar(image, bounds, 46, color)
    return image


def chorus():
    image = canvas("#F3EEE6")
    bars = (
        ((194, 404, 282, 734), "#FF5E70", 14),
        ((342, 262, 430, 742), "#4E7BFF", 7),
        ((468, 208, 556, 798), "#17121F", 0),
        ((594, 262, 682, 742), "#74D99F", -7),
        ((742, 404, 830, 734), "#C177FF", -14),
    )
    for bounds, color, angle in bars:
        bar(image, bounds, 44, color, angle)
    return image


def signal():
    image = canvas("#090D18")
    ImageDraw.Draw(image).rounded_rectangle(box((158, 158, 866, 866)), radius=180 * SCALE, fill="#11162A")
    bars = (
        ((234, 480, 312, 718), "#00C2D7"),
        ((346, 298, 424, 718), "#F04B9C"),
        ((458, 418, 536, 718), "#B9D54A"),
        ((570, 242, 648, 718), "#FF7A3D"),
        ((682, 368, 760, 718), "#7A68FF"),
    )
    for bounds, color in bars:
        bar(image, bounds, 39, color)
    return image


def save(name, image):
    target = ROOT / "brand" / "redirect" / name
    renders = target / "renders"
    renders.mkdir(parents=True, exist_ok=True)
    master = image.resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    master.save(target / "icon-1024.png", optimize=True)
    for size in (16, 32, 128):
        master.resize((size, size), Image.Resampling.LANCZOS).save(renders / f"icon-{size}.png", optimize=True)


def main():
    save("measure", measure())
    save("chorus", chorus())
    save("signal", signal())
    print("Rendered 3 redirected RGBA masters and 9 native-size derivatives.")


if __name__ == "__main__":
    main()
