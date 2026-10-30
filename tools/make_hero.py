#!/usr/bin/env python3
"""Compose the screens into one hero image for the README."""
import os
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SH = os.path.join(HERE, "screenshots")
NAMES = ["1-clock-light.png", "2-clock-dark.png", "3-stopwatch.png",
         "4-timer.png", "5-glass-settings.png"]

W = 300
GAP = 24
PAD = 40
RAD = 24


def rounded(img, rad):
    m = Image.new("L", img.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, img.size[0] - 1, img.size[1] - 1], radius=rad, fill=255)
    out = img.convert("RGBA")
    out.putalpha(m)
    return out


def main():
    imgs = []
    for n in NAMES:
        path = os.path.join(SH, n)
        if not os.path.exists(path):
            continue
        im = Image.open(path).convert("RGB")
        h = int(im.height * W / im.width)
        imgs.append(rounded(im.resize((W, h), Image.LANCZOS), RAD))
    h = imgs[0].height
    total_w = PAD * 2 + W * len(imgs) + GAP * (len(imgs) - 1)
    canvas = Image.new("RGB", (total_w, h + PAD * 2), (246, 247, 251))

    for i, im in enumerate(imgs):
        x = PAD + i * (W + GAP)
        shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow)
        sd.rounded_rectangle([x + 4, PAD + 12, x + W + 4, PAD + h + 12], radius=RAD, fill=(30, 40, 80, 70))
        shadow = shadow.filter(ImageFilter.GaussianBlur(14))
        canvas.paste(Image.alpha_composite(canvas.convert("RGBA"), shadow).convert("RGB"), (0, 0))
        canvas.paste(im, (x, PAD), im)

    out = os.path.join(SH, "hero.png")
    canvas.save(out, optimize=True)
    print("hero", out, canvas.size)


if __name__ == "__main__":
    main()
