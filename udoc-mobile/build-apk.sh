#!/usr/bin/env bash
# Build the UDOC Control signed .apk. RUN ON A MACHINE WITH: Android Studio (or cmdline-tools),
# JDK 17+, Node 18+. App ID: za.gods.udoc
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"

echo "==> 1/5 Build the web app (udoc-app)"
( cd "../udoc-app" && npm install && npm run build )
rm -rf www && mkdir www && cp -r "../udoc-app/dist/"* www/

echo "==> 2/5 Install Capacitor + generate the native android/ project"
npm install
npx cap add android        # creates android/ using the Android SDK
npx cap sync

echo "==> 3/5 Apply G.O.D.S Android resources (network security, strings, permissions)"
RES=android/app/src/main/res
mkdir -p "$RES/xml" "$RES/values"
cp android-resources/xml/network_security_config.xml "$RES/xml/"
cp android-resources/values/strings.xml "$RES/values/"
echo "    NOTE: merge android-resources/AndroidManifest.permissions.xml into"
echo "          android/app/src/main/AndroidManifest.xml (INTERNET + networkSecurityConfig)."

echo "==> 4/5 Build the APK"
cd android
if [ -f ./gradlew ]; then GRADLE=./gradlew; else GRADLE=gradle; fi
$GRADLE assembleRelease          # unsigned release; or assembleDebug for a quick test build
cd ..

echo "==> 5/5 Done"
echo "    Unsigned APK: android/app/build/outputs/apk/release/app-release-unsigned.apk"
echo "    To SIGN for distribution, open in Android Studio:  npx cap open android"
echo "      then Build > Generate Signed Bundle / APK > APK > create keystore > release."
echo "    Or sign from CLI with apksigner (see SDK build-tools)."
