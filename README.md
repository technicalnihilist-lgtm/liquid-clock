# Liquid Clock

A glassy, liquid-blob clock for Android — analog + digital clock, world clock, stopwatch and timer in one offline app.

![Liquid Clock screens](https://raw.githubusercontent.com/technicalnihilist-lgtm/liquid-clock/main/screenshots/hero.png)

Built from a single-page HTML design and wrapped in a native Android WebView shell, so the whole UI is one file you can edit without touching Java.

## Screenshots

| Clock | Clock (dark) | Stopwatch | Timer | Glass settings |
| --- | --- | --- | --- | --- |
| ![Clock](https://raw.githubusercontent.com/technicalnihilist-lgtm/liquid-clock/main/screenshots/1-clock-light.png) | ![Clock dark](https://raw.githubusercontent.com/technicalnihilist-lgtm/liquid-clock/main/screenshots/2-clock-dark.png) | ![Stopwatch](https://raw.githubusercontent.com/technicalnihilist-lgtm/liquid-clock/main/screenshots/3-stopwatch.png) | ![Timer](https://raw.githubusercontent.com/technicalnihilist-lgtm/liquid-clock/main/screenshots/4-timer.png) | ![Glass settings](https://raw.githubusercontent.com/technicalnihilist-lgtm/liquid-clock/main/screenshots/5-glass-settings.png) |

Direct links:

- https://raw.githubusercontent.com/technicalnihilist-lgtm/liquid-clock/main/screenshots/1-clock-light.png
- https://raw.githubusercontent.com/technicalnihilist-lgtm/liquid-clock/main/screenshots/2-clock-dark.png
- https://raw.githubusercontent.com/technicalnihilist-lgtm/liquid-clock/main/screenshots/3-stopwatch.png
- https://raw.githubusercontent.com/technicalnihilist-lgtm/liquid-clock/main/screenshots/4-timer.png
- https://raw.githubusercontent.com/technicalnihilist-lgtm/liquid-clock/main/screenshots/5-glass-settings.png

App icon: https://raw.githubusercontent.com/technicalnihilist-lgtm/liquid-clock/main/icon.png

## Features

- **Clock** — smooth sweeping analog face (60fps, sub-second hands), big digital readout, 12/24-hour toggle that is remembered, date line
- **World clock** — Mumbai, London, New York, Dubai, Tokyo, Sydney with Today / Tomorrow / Yesterday labels relative to your own date
- **Stopwatch** — start / stop / lap / reset, split times per lap
- **Timer** — 1, 5, 10 and 25 minute presets, circular progress ring, pause / resume / reset, beep + vibration when it finishes, and the alarm fires even if you are on another tab
- **Glass settings** — a bottom sheet with live sliders for transparency, blur, vibrancy, shine and background glow; your mix is saved
- **Motion** — spring-eased tab transitions, a sliding glass lens you can drag between the three tabs, staggered content reveals and iOS-style rubber-band overscroll
- **Dark mode** — follows the system setting live, no restart needed
- **Edge to edge** — draws under the status and navigation bars, correct insets on notched phones
- **Offline** — no internet permission at all, everything runs from local assets
- **State survives** — stopwatch and timer keep running across app switches and relaunches (wall-clock based, not frame based)
- **Back button** — closes the settings sheet first, then returns to the Clock tab, then exits

## Install

**[Download LiquidClock-1.1.0.apk](https://github.com/technicalnihilist-lgtm/liquid-clock/releases/latest/download/LiquidClock-1.1.0.apk)** and open it on your phone. You will need to allow install from unknown sources, since this is a self-signed build rather than a Play Store release.

- Minimum Android 6.0 (API 23), targets Android 14 (API 34)
- Size ~258 KB, no dependencies, no internet permission

Newer builds are published on the [Releases](https://github.com/technicalnihilist-lgtm/liquid-clock/releases) page; the same copy also sits in `releases/` in the repo.

## Changelog

### 1.1.0
- Glass settings sheet: transparency, blur, vibrancy, shine and background glow sliders, remembered across launches
- Draggable glass lens in the bottom navigation, spring-eased tab and content transitions
- Rubber-band overscroll on scrollable pages
- Timer completion is now checked on every tab, not just while the Timer tab is open
- Single rAF loop with change-guarded text updates, so the clock stops re-writing the DOM 60 times a second
- Version name and code are now build parameters (`VER`, `VCODE`)

### 1.0.0
- First release: clock, world clock, stopwatch, timer, dark mode, edge-to-edge, persistent state

## Build

No Gradle needed — the APK is assembled with the Android SDK command line tools.

```bash
export ANDROID_HOME=$HOME/Android/Sdk   # needs build-tools;34.0.0 and platforms;android-34
VER=1.1.0 VCODE=2 bash build.sh
```

The output lands in `build/LiquidClock-<version>.apk`. The first run generates a signing key at `keystore/liquidclock.jks`; keep that file, because Android only accepts updates signed with the same key.

Screenshots are generated from the real UI with headless Chromium:

```bash
pip install playwright
python3 tools/make_screenshots.py
python3 tools/make_hero.py
```

## Project layout

```
assets/index.html          the entire UI (HTML + CSS + JS, no build step)
src/.../MainActivity.java  native shell: WebView, insets, theme, vibration, back
res/                       icons, theme, strings
AndroidManifest.xml        permissions: VIBRATE only
build.sh                   aapt2 -> javac -> d8 -> zipalign -> apksigner
tools/make_icons.py        generates launcher icons
tools/make_screenshots.py  renders screenshots from assets/index.html
```

## Design notes

The palette, glass panels, floating blobs and the orange accent are unchanged from the original design. What changed for the app version: the three nav icons are inline SVG instead of emoji (so they render the same on every OEM), safe-area insets come from the native layer, the 12/24-hour choice, running timers and glass settings persist, and the world clock list starts with Mumbai.

## License

MIT
