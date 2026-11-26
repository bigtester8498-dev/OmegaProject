#!/usr/bin/env python3
"""Draws the placeholder icon: a dark rounded square with a white Omega sign (needs Pillow).

  python tools/make_icon.py [--font FILE]

Writes launcher/OmegaLauncher/omega.ico (16 to 256 px) and site/favicon.png (64 px), site/icon.png (256 px).
Each size is drawn on its own from a 4x canvas, so the small sizes stay sharp. Replace it when the game has art.
"""

import argparse
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
ICO = os.path.join(ROOT, "launcher", "OmegaLauncher", "omega.ico")
FAVICON = os.path.join(ROOT, "site", "favicon.png")
ICON = os.path.join(ROOT, "site", "icon.png")
SIZES = [16, 24, 32, 48, 64, 128, 256]
BACK = (24, 26, 32, 255)
EDGE = (70, 76, 90, 255)
FORE = (255, 255, 255, 255)
FONTS = [r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\segoeuib.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
OMEGA = "\u03a9"


def find_font(explicit):
    for path in ([explicit] if explicit else []) + FONTS:
        if path and os.path.isfile(path):
            return path
    raise SystemExit("no font found; pass --font FILE (a TTF with the Greek capital Omega)")


def draw(size, font_path):
    k = 4
    big = size * k
    img = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    radius = big // 6
    border = max(k, big // 40)
    d.rounded_rectangle([0, 0, big - 1, big - 1], radius=radius, fill=EDGE)
    d.rounded_rectangle([border, border, big - 1 - border, big - 1 - border], radius=radius - border, fill=BACK)
    font = ImageFont.truetype(font_path, int(big * 0.72))
    left, top, right, bottom = d.textbbox((0, 0), OMEGA, font=font)
    x = (big - (right - left)) / 2 - left
    y = (big - (bottom - top)) / 2 - top
    d.text((x, y), OMEGA, font=font, fill=FORE)
    return img.resize((size, size), Image.LANCZOS)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--font")
    a = ap.parse_args()
    font = find_font(a.font)
    images = {s: draw(s, font) for s in SIZES}
    os.makedirs(os.path.dirname(ICO), exist_ok=True)
    images[256].save(ICO, format="ICO", sizes=[(s, s) for s in SIZES],
                     append_images=[images[s] for s in SIZES if s != 256])
    os.makedirs(os.path.dirname(FAVICON), exist_ok=True)
    images[64].save(FAVICON, format="PNG", optimize=True)
    images[256].save(ICON, format="PNG", optimize=True)
    print("wrote %s, %s, %s" % (ICO, FAVICON, ICON))


if __name__ == "__main__":
    main()
