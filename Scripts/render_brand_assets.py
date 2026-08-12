#!/usr/bin/env python3
"""Rasterize the three geometric BRAND.1 icon directions with transparent corners."""

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
SCALE = 4
SIZE = 1024

CANVAS = "#09090B"
SURFACE = "#111114"
RAISED = "#19191D"
LINE = "#323238"
TEXT = "#F4F1EA"
ACCENT = "#F2A64A"
ACCENT_HOVER = "#FFC06B"


def scaled(values):
    return tuple(round(value * SCALE) for value in values)


def make_canvas():
    image = Image.new("RGBA", (SIZE * SCALE, SIZE * SCALE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle(scaled((64, 64, 960, 960)), radius=224 * SCALE, fill=SURFACE)
    return image, draw


def crack():
    image, draw = make_canvas()
    draw.rounded_rectangle(scaled((148, 196, 876, 828)), radius=64 * SCALE, fill=RAISED)
    draw.polygon([scaled(point) for point in ((206, 202), (716, 202), (472, 822), (206, 822), (154, 770), (154, 254))], fill=CANVAS)
    draw.polygon([scaled(point) for point in ((715, 202), (751, 202), (504, 822), (469, 822))], fill=ACCENT)
    return image


def mirror():
    image, draw = make_canvas()
    draw.ellipse(scaled((190, 190, 834, 834)), fill=CANVAS)
    draw.ellipse(scaled((260, 260, 764, 764)), fill=RAISED)
    draw.polygon([scaled(point) for point in ((667, 287), (710, 319), (744, 360), (766, 408), (720, 362), (665, 334), (602, 321), (624, 304), (646, 292))], fill=ACCENT)
    draw.ellipse(scaled((651, 308, 719, 376)), fill=ACCENT_HOVER)
    return image


def rhythm():
    image, draw = make_canvas()
    bars = (
        ((214, 330, 286, 694), LINE),
        ((345, 252, 417, 772), TEXT),
        ((476, 384, 548, 640), LINE),
        ((607, 294, 679, 730), ACCENT),
        ((738, 356, 810, 668), LINE),
    )
    for box, color in bars:
        draw.rounded_rectangle(scaled(box), radius=36 * SCALE, fill=color)
    return image


def save_direction(name, image):
    target = ROOT / "brand" / "directions" / name
    master = image.resize((SIZE, SIZE), Image.Resampling.LANCZOS)
    master.save(target / "icon-1024.png", optimize=True)
    for size in (16, 32, 128):
        rendered = master.resize((size, size), Image.Resampling.LANCZOS)
        rendered.save(target / "renders" / f"icon-{size}.png", optimize=True)

    evidence = Image.new("RGB", (420, 220), CANVAS)
    evidence_draw = ImageDraw.Draw(evidence)
    x_positions = {16: 32, 32: 92, 128: 246}
    baseline = 170
    for size in (16, 32, 128):
        icon = Image.open(target / "renders" / f"icon-{size}.png").convert("RGBA")
        x = x_positions[size]
        evidence.alpha_composite(icon, (x, baseline - size)) if evidence.mode == "RGBA" else evidence.paste(icon, (x, baseline - size), icon)
        evidence_draw.text((x, 188), str(size), fill="#969188")
    evidence_draw.text((32, 24), f"{name.title()} — actual pixels", fill="#F4F1EA")
    evidence.save(ROOT / "docs" / "reviews" / "BRAND.1" / "screenshots" / f"{name}-sizes.png", optimize=True)


def main():
    save_direction("crack", crack())
    save_direction("mirror", mirror())
    save_direction("rhythm", rhythm())
    print("Rendered 3 transparent 1024px masters and 9 size derivatives.")


if __name__ == "__main__":
    main()
