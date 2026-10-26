#!/usr/bin/env python3
"""Generate Liquid Clock launcher icons (legacy + adaptive foreground)."""
import math, os
from PIL import Image, ImageDraw, ImageFilter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SS = 4  # supersample factor

DENS = {"mdpi": 1.0, "hdpi": 1.5, "xhdpi": 2.0, "xxhdpi": 3.0, "xxxhdpi": 4.0}


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def gradient(size, c1, c2, c3):
    img = Image.new("RGB", (size, size))
    d = ImageDraw.Draw(img)
    for y in range(size):
        t = y / max(1, size - 1)
        col = lerp(c1, c2, t / 0.55) if t < 0.55 else lerp(c2, c3, (t - 0.55) / 0.45)
        d.line([(0, y), (size, y)], fill=col)
    return img


def draw_clock(size, pad_ratio, transparent_bg=True, rounded_mask=False):
    """Return RGBA icon of `size` px. pad_ratio = margin around the clock face."""
    S = size * SS
    canvas = Image.new("RGBA", (S, S), (0, 0, 0, 0))

    # soft liquid blobs background
    bg = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    grad = gradient(S, (122, 162, 255), (255, 143, 208), (127, 232, 209)).convert("RGBA")
    bg.paste(grad, (0, 0))

    if rounded_mask:
        mask = Image.new("L", (S, S), 0)
        ImageDraw.Draw(mask).ellipse([0, 0, S - 1, S - 1], fill=255)
        bg.putalpha(mask)
    canvas.alpha_composite(bg)

    # glass face
    pad = int(S * pad_ratio)
    box = [pad, pad, S - pad, S - pad]
    face = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    fd = ImageDraw.Draw(face)
    fd.ellipse(box, fill=(255, 255, 255, 105), outline=(255, 255, 255, 205), width=max(2, S // 90))
    canvas.alpha_composite(face)

    cx = cy = S / 2
    r = (S - 2 * pad) / 2

    d = ImageDraw.Draw(canvas)

    # tick marks
    for i in range(60):
        a = math.radians(i * 6)
        big = i % 5 == 0
        r1 = r * (0.84 if big else 0.90)
        r2 = r * 0.96
        w = max(2, int(S * (0.011 if big else 0.004)))
        col = (11, 12, 20, 225) if big else (11, 12, 20, 110)
        d.line([(cx + r1 * math.sin(a), cy - r1 * math.cos(a)),
                (cx + r2 * math.sin(a), cy - r2 * math.cos(a))], fill=col, width=w)

    def hand(angle_deg, length, width, color):
        a = math.radians(angle_deg)
        x = cx + length * math.sin(a)
        y = cy - length * math.cos(a)
        d.line([(cx, cy), (x, y)], fill=color, width=width)
        rr = width / 2
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=color)

    ink = (11, 12, 20, 255)
    orange = (255, 159, 10, 255)
    hand(300, r * 0.50, max(3, int(S * 0.030)), ink)      # hour ~10
    hand(60,  r * 0.72, max(2, int(S * 0.021)), ink)      # minute ~2
    hand(150, r * 0.80, max(2, int(S * 0.010)), orange)   # second ~5

    # centre pin
    pr = S * 0.026
    d.ellipse([cx - pr, cy - pr, cx + pr, cy + pr], fill=orange)

    return canvas.resize((size, size), Image.LANCZOS)


def main():
    for name, mult in DENS.items():
        folder = os.path.join(BASE, "res", "mipmap-" + name)
        os.makedirs(folder, exist_ok=True)

        legacy = int(48 * mult)
        draw_clock(legacy, 0.09).save(os.path.join(folder, "ic_launcher.png"))
        draw_clock(legacy, 0.09, rounded_mask=True).save(os.path.join(folder, "ic_launcher_round.png"))

        fg = int(108 * mult)
        draw_clock(fg, 0.235).save(os.path.join(folder, "ic_launcher_fg.png"))
        print("wrote", folder, legacy, fg)


if __name__ == "__main__":
    main()
