#!/usr/bin/env python3
"""Generate Liquid Clock launcher icons from assets/icon-source.png.

Writes the legacy mipmaps (rounded + round variants) and the adaptive-icon
foreground layer for every density. Edit assets/icon-source.png and re-run:

    python3 tools/make_icons.py
"""
import os

from PIL import Image, ImageDraw

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, "assets", "icon-source.png")
DENS = {"mdpi": 1.0, "hdpi": 1.5, "xhdpi": 2.0, "xxhdpi": 3.0, "xxxhdpi": 4.0}
SS = 4  # supersample factor for the circle mask


def art(size):
    return Image.open(SRC).convert("RGBA").resize((size, size), Image.LANCZOS)


def circle_mask(size):
    mask = Image.new("L", (size * SS, size * SS), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, size * SS - 1, size * SS - 1], fill=255)
    return mask.resize((size, size), Image.LANCZOS)


def main():
    for name, mult in DENS.items():
        folder = os.path.join(BASE, "res", "mipmap-" + name)
        os.makedirs(folder, exist_ok=True)

        legacy = int(48 * mult)
        art(legacy).save(os.path.join(folder, "ic_launcher.png"))

        round_icon = art(legacy)
        round_icon.putalpha(circle_mask(legacy))
        round_icon.save(os.path.join(folder, "ic_launcher_round.png"))

        fg = int(108 * mult)
        art(fg).save(os.path.join(folder, "ic_launcher_fg.png"))
        print("wrote", folder, legacy, fg)


if __name__ == "__main__":
    main()
