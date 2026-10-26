#!/usr/bin/env python3
"""Render Liquid Clock screens at phone resolution for the README / release."""
import os, glob
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = "file://" + os.path.join(HERE, "assets", "index.html")
OUT = os.path.join(HERE, "screenshots")
os.makedirs(OUT, exist_ok=True)

W, H = 412, 915  # CSS px, Pixel-class phone


def launch(p):
    try:
        return p.chromium.launch()
    except Exception:
        cand = glob.glob("/opt/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell")
        if not cand:
            raise
        return p.chromium.launch(executable_path=sorted(cand)[-1])


def main():
    with sync_playwright() as p:
        b = launch(p)
        ctx = b.new_context(viewport={"width": W, "height": H}, device_scale_factor=2.625,
                            is_mobile=True, has_touch=True, locale="en-IN",
                            timezone_id="Asia/Kolkata")
        pg = ctx.new_page()
        pg.goto(APP)
        pg.wait_for_timeout(1200)

        shots = []

        # 1 - clock, light
        pg.evaluate("window.__setDark(false)")
        pg.wait_for_timeout(900)
        f = os.path.join(OUT, "1-clock-light.png"); pg.screenshot(path=f); shots.append(f)

        # 2 - clock, dark
        pg.evaluate("window.__setDark(true)")
        pg.wait_for_timeout(900)
        f = os.path.join(OUT, "2-clock-dark.png"); pg.screenshot(path=f); shots.append(f)
        pg.evaluate("window.__setDark(false)")

        # 3 - stopwatch running with laps
        pg.click('nav button[data-t="sw"]')
        pg.wait_for_timeout(350)
        pg.click("#sg")
        pg.wait_for_timeout(1500)
        pg.click("#sl")
        pg.wait_for_timeout(1700)
        pg.click("#sl")
        pg.wait_for_timeout(700)
        f = os.path.join(OUT, "3-stopwatch.png"); pg.screenshot(path=f); shots.append(f)

        # 4 - timer running
        pg.click('nav button[data-t="tm"]')
        pg.wait_for_timeout(350)
        pg.click('button[data-m="5"]')
        pg.wait_for_timeout(250)
        pg.click("#tg")
        pg.wait_for_timeout(1600)
        f = os.path.join(OUT, "4-timer.png"); pg.screenshot(path=f); shots.append(f)

        ctx.close(); b.close()
        for s in shots:
            print("shot", os.path.basename(s), os.path.getsize(s))


if __name__ == "__main__":
    main()
