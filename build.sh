#!/usr/bin/env bash
# Build, align and sign Liquid Clock without Gradle.
# Requires: JDK 17+, Android SDK build-tools 34.0.0 + platforms/android-34.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
: "${ANDROID_HOME:=$HOME/Android/Sdk}"
: "${JAVA_HOME:=$(dirname "$(dirname "$(readlink -f "$(command -v javac)")")")}"
BT="$ANDROID_HOME/build-tools/34.0.0"
export PATH="$JAVA_HOME/bin:$PATH"
PLATFORM="$ANDROID_HOME/platforms/android-34/android.jar"
OUT="$ROOT/build"
KEYSTORE="${KEYSTORE:-$ROOT/keystore/liquidclock.jks}"
KS_PASS="${KS_PASS:-liquidclock}"
VER="${VER:-1.1.0}"
VCODE="${VCODE:-2}"

rm -rf "$OUT"
mkdir -p "$OUT/res" "$OUT/classes" "$OUT/dex"

python3 "$ROOT/tools/make_icons.py"

echo "==> aapt2 compile"
"$BT/aapt2" compile --dir "$ROOT/res" -o "$OUT/res/resources.zip"

echo "==> aapt2 link"
"$BT/aapt2" link \
  -o "$OUT/base.apk" \
  -I "$PLATFORM" \
  --manifest "$ROOT/AndroidManifest.xml" \
  -R "$OUT/res/resources.zip" \
  -A "$ROOT/assets" \
  --java "$OUT/gen" \
  --min-sdk-version 23 \
  --target-sdk-version 34 \
  --version-code "$VCODE" --version-name "$VER" \
  --auto-add-overlay

echo "==> javac"
mkdir -p "$OUT/gen"
find "$ROOT/src" "$OUT/gen" -name '*.java' > "$OUT/sources.txt"
"$JAVA_HOME/bin/javac" -nowarn -Xlint:none --release 11 -classpath "$PLATFORM" \
  -d "$OUT/classes" @"$OUT/sources.txt"

echo "==> d8"
find "$OUT/classes" -name '*.class' > "$OUT/classes.txt"
"$BT/d8" --lib "$PLATFORM" --min-api 23 --release \
  --output "$OUT/dex" @"$OUT/classes.txt"

echo "==> package"
cp "$OUT/base.apk" "$OUT/unsigned.apk"
(cd "$OUT/dex" && zip -q -X "$OUT/unsigned.apk" classes.dex)

echo "==> zipalign"
"$BT/zipalign" -f -p 4 "$OUT/unsigned.apk" "$OUT/aligned.apk"

if [ ! -f "$KEYSTORE" ]; then
  echo "==> generating signing key"
  mkdir -p "$(dirname "$KEYSTORE")"
  "$JAVA_HOME/bin/keytool" -genkeypair -v -keystore "$KEYSTORE" -alias liquidclock \
    -keyalg RSA -keysize 2048 -validity 10950 \
    -storepass "$KS_PASS" -keypass "$KS_PASS" \
    -dname "CN=Liquid Clock, OU=Mobile, O=Liquid Clock, L=Mumbai, S=MH, C=IN" >/dev/null 2>&1
fi

echo "==> apksigner"
"$BT/apksigner" sign --ks "$KEYSTORE" --ks-key-alias liquidclock \
  --ks-pass "pass:$KS_PASS" --key-pass "pass:$KS_PASS" \
  --v1-signing-enabled true --v2-signing-enabled true \
  --out "$OUT/LiquidClock-$VER.apk" "$OUT/aligned.apk"

"$BT/apksigner" verify --print-certs "$OUT/LiquidClock-$VER.apk" | head -5
ls -lh "$OUT/LiquidClock-$VER.apk"
