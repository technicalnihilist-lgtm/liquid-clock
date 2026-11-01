# Daily optimisation run — operating instructions

This file is the runbook for the scheduled 1 → 20 November series. Each daily run follows it top to bottom.

## 0. What a run must produce

Ten small, invisible improvements from `ROADMAP.md` for today's date, each built into a signed APK, pushed to `technicalnihilist-lgtm/liquid-clock`, and attached to that day's release. Plus a short honest report.

**Non-negotiable:** no visual change. No layout, spacing, colour, typography, copy, icon, motion-feel or screen-flow change. If a fix would be visible, skip it, leave it unticked, and mention it in the report.

## 1. Work out the day

Today's date in `Asia/Kolkata` gives the day number (1 Nov = day 1, 20 Nov = day 20). Open `ROADMAP.md`, find that day's section, and take its ten unticked items.

If today is after 20 November 2026, do nothing and report that the series is closed.

## 2. Get the project into the sandbox

The sandbox is wiped between runs, so start from the repo every time:

```
fetch_repo(owner="technicalnihilist-lgtm", repo="liquid-clock")
```

This lands in `/scratch/repos/liquid-clock`. Work there.

Then restore the signing key — it is deliberately **not** in the repo:

```
mkdir -p /scratch/repos/liquid-clock/keystore
cp /scratch/saved/liquidclock-signing-key.jks /scratch/repos/liquid-clock/keystore/liquidclock.jks
```

`cp /scratch/saved/...` is read-only and safe. Never commit the keystore.

## 3. Make sure the Android toolchain exists

```
ls /scratch/work/sdk/jdk-*/bin/java
ls /scratch/work/sdk/android-sdk/build-tools/34.0.0/aapt2
```

If either is missing, install once per run (~3 minutes):

```
mkdir -p /scratch/work/sdk && cd /scratch/work/sdk
curl -sSL -o jdk.tar.gz "https://api.adoptium.net/v3/binary/latest/17/ga/linux/x64/jdk/hotspot/normal/eclipse"
tar xzf jdk.tar.gz
curl -sSL -o cmdline.zip "https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip"
unzip -q cmdline.zip -d .
mkdir -p android-sdk/cmdline-tools && mv cmdline-tools android-sdk/cmdline-tools/latest
ulimit -v unlimited
export JAVA_HOME=$(echo /scratch/work/sdk/jdk-*)
export ANDROID_HOME=/scratch/work/sdk/android-sdk
yes | $ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --sdk_root=$ANDROID_HOME --licenses >/dev/null
$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager --sdk_root=$ANDROID_HOME "platforms;android-34" "build-tools;34.0.0"
```

**Every command that runs Java needs `ulimit -v unlimited` first** — the sandbox ships a 1.5 GB virtual-memory cap that kills the JVM otherwise.

## 4. Implement the day's items

Edit `assets/index.html` (the whole UI), `src/com/liquidclock/app/MainActivity.java` (the native shell) or `build.sh`, depending on the item. One item at a time, smallest possible diff.

After each item, bump the version and build:

```
ulimit -v unlimited
export JAVA_HOME=$(echo /scratch/work/sdk/jdk-*)
export ANDROID_HOME=/scratch/work/sdk/android-sdk
export JAVA_OPTS="-Xmx768m -XX:CompressedClassSpaceSize=256m"
VER=1.<day+2>.<n> VCODE=<3 + (day-1)*10 + n> bash build.sh
```

Day 1 → `1.3.1`…`1.3.10`, versionCode 4…13. Day 2 → `1.4.1`…`1.4.10`, versionCode 14…23. And so on; day 20 ends at versionCode 203.

Verify every build:

```
$ANDROID_HOME/build-tools/34.0.0/apksigner verify --print-certs build/LiquidClock-<VER>.apk
```

The certificate SHA-256 must stay `a1e7d5e8406da47008a2acd740c6ec270a7e0ee74abe492b7e34d7a638f4a104`. If it changes, the keystore was not restored — stop and fix before publishing, otherwise nobody can install the update.

Render-check the UI after the changes (this also catches a broken layout from an "invisible" fix):

```
pip install --quiet playwright
export PLAYWRIGHT_BROWSERS_PATH=/opt/ms-playwright
python3 tools/make_screenshots.py
```

Then **compare against the previous day's screenshots**. Any pixel difference in layout, colour or copy is a regression — revert that item.

## 5. Publish

`git push` is refused for this repo (the App token is scoped elsewhere), so publish through the API:

1. `GITHUB_COMMIT_MULTIPLE_FILES` — one commit with the changed files (base64 for binaries, utf-8 for text) and a message naming the items, e.g. `perf(1.3.4): cache dayWord formatters, drop per-second allocation`.
2. Put the day's final APK in `releases/` in the repo as well, so the repo always carries the latest build.
3. Tick the items in `ROADMAP.md` and include it in a commit.
4. Create the day's release once per day: tag `v1.<day+2>.10`, title `Liquid Clock 1.<day+2> — day <day>`, body listing the ten items.
5. Attach all ten APKs to that release:
   - `cp build/LiquidClock-<VER>.apk /scratch/output/` (the upload tool only accepts saved files),
   - `upload(toolkit="github", tool_slug="GITHUB_UPLOAD_RELEASE_ASSET", path="/scratch/output/LiquidClock-<VER>.apk")`,
   - pass the returned `s3key` to `GITHUB_UPLOAD_RELEASE_ASSET` with `release_id` and `content_type="application/vnd.android.package-archive"`.

## 6. Report

End the run with a short report, not a wall of text:

- day number and date
- the ten items, each marked done / deferred (with one-line reason)
- any bug found while working, and whether it was fixed
- final version name and versionCode, APK size, signature digest
- the measured numbers the day asked for (fps, frame budget, startup, memory — whichever apply)

## 7. When things go wrong

- **A build fails:** fix it, do not skip. A broken build is never published.
- **An item turns out to need a visible change:** revert it, leave it unticked, say why.
- **Time runs short:** publish the items that are finished and verified, record the rest as still unticked in `ROADMAP.md`, and say plainly how many of the ten were completed. Never mark an item done that is not in the shipped APK.
- **The repo or API is unreachable:** stop, do not fake a release, and report the failure.

## 8. Baseline to protect

- Package `com.liquidclock.app`, minSdk 23, targetSdk 34, only the `VIBRATE` permission.
- UI identical to the 1.2.0 build: same three tabs, same glass settings sheet, same colours and spacing.
- APK around 258 KB. Growing past 300 KB means something crept in that should not have.
