#!/usr/bin/env bash
# Build the unified "G.O.D.S UDOC" mobile gateway APK. App ID: za.gods.udoc.gateway
# OTA shell: loads https://gods-udoc-gateway.onrender.com (server.url). www/ is only an offline splash.
# RUN ON A MACHINE WITH: Android Studio (or cmdline-tools), JDK 17+, Node 18+.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"; cd "$HERE"
echo "==> 1/4 Install Capacitor + generate android/"
npm install
npx cap add android
npx cap sync
echo "==> 2/4 Apply G.O.D.S Android resources"
RES=android/app/src/main/res
mkdir -p "$RES/xml" "$RES/values"
cp android-resources/xml/network_security_config.xml "$RES/xml/"
cp android-resources/values/strings.xml "$RES/values/"
echo "    NOTE: merge android-resources/AndroidManifest.permissions.xml into android/app/src/main/AndroidManifest.xml"
echo "==> 3/4 Build the APK"
cd android; if [ -f ./gradlew ]; then G=./gradlew; else G=gradle; fi; $G assembleRelease; cd ..
echo "==> 4/4 Done -> android/app/build/outputs/apk/release/app-release-unsigned.apk"
echo "    Sign for distribution:  npx cap open android  (Build > Generate Signed Bundle/APK)"
