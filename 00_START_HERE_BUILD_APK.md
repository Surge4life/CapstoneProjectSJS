> **Pre-registration forecast.** G.O.D.S Holdings (Pty) Ltd is a *proposed* entity — not registered. No trust, trademark, or domain is registered; all IP vests in Sashin J. Singh. See `BRAND_AND_ENTITY_CONSTANTS.md` and `PRE_REGISTRATION_NOTICE.md`.

# 00_START_HERE — Build your first G.O.D.S app (.apk), start to finish (Windows)

This takes you from **nothing open** to a working **UDOC `.apk`** installed on a phone.
Your backend is already live on Render, so the app will connect to it automatically.

Keep this open on your phone or a second window while you work on the desktop.

> **Set expectations:** the first Android build almost always stops at ONE snag (usually the
> SDK location). That is normal. Each snag has a fix in the **Cheat-Sheet** at the bottom.
> Don't panic at red text — read which error it is, apply the fix, continue.

---

## WHAT YOU NEED (we verify each as we go)
- Windows PC ✓ (you have)
- Android Studio installed ✓ (you have)
- Node.js 18+  → we verify in Phase 2
- The project files on your desktop → Phase 1

---

## PHASE 1 — Get the project files onto your desktop

1. Download the latest **GODS_ECOSYSTEM.zip** (the one shared in chat).
2. Move it to your **Desktop** (so the path is short and easy).
3. Right-click → **Extract All** → extract to the Desktop.
   You now have a folder: `C:\Users\<you>\Desktop\GODS_ECOSYSTEM`
4. Open it and confirm you see folders like `udoc-mobile`, `platform-core`, `seths-app`, plus
   files like `render.yaml` and `00_PROGRESS.md`.

✅ Done when: the `GODS_ECOSYSTEM` folder is on your Desktop and you can see `udoc-mobile` inside.

---

## PHASE 2 — Verify Node.js is installed

1. Press **Windows key**, type `cmd`, open **Command Prompt**.
2. Type and Enter:
   ```
   node --version
   ```
   - **If you see a version** like `v20.x.x` → good, skip to Phase 3.
   - **If it says "not recognized"** → install Node:
     - Go to https://nodejs.org → download the **LTS** version → run the installer →
       accept defaults → finish. Close and reopen Command Prompt, run `node --version` again.

✅ Done when: `node --version` prints a number (v18 or higher).

---

## PHASE 3 — Open a terminal inside the udoc-mobile folder

1. In File Explorer, go into: `Desktop\GODS_ECOSYSTEM\udoc-mobile`
2. Click the **address bar** at the top (where the folder path shows), type `cmd`, press **Enter**.
   A black terminal opens, already "inside" the udoc-mobile folder.
3. Confirm you're in the right place — type:
   ```
   dir
   ```
   You should see: `capacitor.config.json`, `package.json`, `www`, `android-resources`, `build-apk.sh`.

✅ Done when: `dir` shows those files.

---

## PHASE 4 — Install the app's dependencies

In that terminal:
```
npm install
```
- Downloads Capacitor and tools into a `node_modules` folder.
- Takes 1–3 minutes. You'll see a progress spinner, then it returns to the prompt.
- Some yellow "warnings" are fine. Only **red "ERR!"** matters.

✅ Done when: it finishes and you're back at the `>` prompt with no red ERR.

---

## PHASE 5 — Generate the native Android project

```
npx cap add android
```
- This creates an `android` folder — the actual native project Android Studio will build.
- If it asks to install the `@capacitor/android` package, type `y` and Enter.

⚠️ **Most common first error here:** `SDK location not found`.
If you see that → go to **Cheat-Sheet → Fix A** below, do it, then run `npx cap add android` again.

✅ Done when: an `android` folder now exists (run `dir` to confirm).

---

## PHASE 6 — Sync your app into the Android project

```
npx cap sync
```
- Copies your built web app (the `www` folder) and plugins into the `android` project.
- Quick — under a minute.

✅ Done when: it prints "sync finished" / returns to the prompt.

> **Note on the `android-resources/` folder and HTTPS:** your UDOC app talks to the live
> backend over **HTTPS** (`https://gods-platform-core.onrender.com`), which works out of the
> box. You can **SKIP** copying android-resources for this first build. Only do that step later
> if you point the app at a plain-http LAN address (see Cheat-Sheet → Fix E).

---

## PHASE 7 — Open the project in Android Studio

```
npx cap open android
```
- Android Studio launches and opens the `android` project.
- **It will start a "Gradle sync"** — a progress bar at the bottom. The FIRST time this can take
  **5–15 minutes** because it downloads Gradle and dependencies. **Let it finish.** Do not click
  Build until the bottom bar is idle and says sync finished.

⚠️ If it pops up **"Android Gradle Plugin upgrade recommended"** → you can click **"Don't remind me
again for this project"** or accept; either is usually fine for a debug build.

⚠️ If sync fails with a **JDK** or **SDK platform** message → Cheat-Sheet → Fix B / Fix C.

✅ Done when: Gradle sync completes (bottom bar idle, no red banner).

---

## PHASE 8 — Build the APK

In Android Studio's top menu:
1. **Build → Build Bundle(s) / APK(s) → Build APK(s)**
2. Wait for the build (a minute or two). A notification appears at the bottom-right:
   **"APK(s) generated successfully"** with a **locate** link.
3. Click **locate**. It opens the folder containing:
   ```
   android\app\build\outputs\apk\debug\app-debug.apk
   ```

🎉 **That `app-debug.apk` is your installable app.**

✅ Done when: `app-debug.apk` exists in that folder.

---

## PHASE 9 — Put it on a phone and run it

**Option 1 — Test on the built-in emulator (no phone needed):**
- In Android Studio, top toolbar, pick a virtual device (or create one via Device Manager) →
  press the green **Run ▶**. The app opens in the emulator.

**Option 2 — Install on your real Android phone:**
1. Copy `app-debug.apk` to your phone (USB cable, Google Drive, or email it to yourself).
2. On the phone, tap the file. Android will warn about "unknown sources" →
   allow installing from this source (Settings prompt) → Install.
3. Open the app. It loads the UDOC Control screen and **connects to your live backend**.
4. Sign in with `admin@gods.local` / `admin123` → you're controlling AIs from your phone, live.

🎉 **That's a real, installed, working app talking to your deployed ecosystem.**

---

## CHEAT-SHEET — the snags and their exact fixes

### Fix A — "SDK location not found"
Capacitor doesn't know where your Android SDK is. Tell it:
1. Find your SDK path: in Android Studio → **File → Settings → Languages & Frameworks →
   Android SDK** (or **Appearance & Behavior → System Settings → Android SDK**). Copy the
   "Android SDK Location" path. It's usually:
   `C:\Users\<you>\AppData\Local\Android\Sdk`
2. In the `android` folder, create a file named **`local.properties`** containing one line
   (use DOUBLE backslashes):
   ```
   sdk.dir=C:\\Users\\<you>\\AppData\\Local\\Android\\Sdk
   ```
   (Replace `<you>` with your Windows username.)
3. Re-run the command that failed.

### Fix B — Gradle JDK / Java version error
Android needs JDK 17+. Android Studio bundles one — point Gradle at it:
- **File → Settings → Build, Execution, Deployment → Build Tools → Gradle**
- Set **Gradle JDK** to the bundled **jbr-17** (or any JDK 17). Click OK, let it re-sync.

### Fix C — "Failed to find Platform SDK" / "SDK Platform not installed"
- Android Studio → **Tools → SDK Manager → SDK Platforms** tab → tick the latest **Android API**
  (e.g. API 34) → Apply → let it download. Also **SDK Tools** tab → ensure **Android SDK
  Build-Tools** and **Android SDK Platform-Tools** are checked → Apply.

### Fix D — "ANDROID_HOME is not set" (only if a command needs it)
Set it for the session in your terminal (adjust the path to your SDK):
```
set ANDROID_HOME=C:\Users\<you>\AppData\Local\Android\Sdk
```
(Permanent: search Windows for "environment variables" → add `ANDROID_HOME` pointing at the SDK.)

### Fix E — App can't reach a plain-http (LAN) backend
Only needed if you point the app at `http://<ip>:8000` instead of the HTTPS Render URL.
Copy the prepared files in after `npx cap add android`:
- `android-resources\xml\network_security_config.xml` → `android\app\src\main\res\xml\`
- `android-resources\values\strings.xml` → `android\app\src\main\res\values\`
- Merge the two lines from `android-resources\AndroidManifest.permissions.xml` into
  `android\app\src\main\AndroidManifest.xml` (INTERNET permission + `networkSecurityConfig`).
For the live HTTPS backend you do NOT need this.

### Fix F — Gradle sync "stuck" / taking forever
First sync genuinely downloads a lot. Give it 10–15 min on a normal connection. If it truly
hangs, **File → Invalidate Caches / Restart**, then let it sync again.

---

## AFTER YOUR FIRST APK

- **Signed release APK (for sharing/Play Store):** Android Studio → **Build → Generate Signed
  Bundle / APK → APK** → create a keystore (save it safely — you reuse it for updates) → release.
  Output: `android\app\build\outputs\apk\release\`.
- **Build the other apps:** repeat Phases 3–8 in `seths-mobile`, `madiba-mobile`, `ts-mobile`,
  `portals-mobile`. (Those connect to the portals/backend per their config.)
- **Desktop `.exe`:** see `00_BUILD_DESKTOP_APPS.md`.

---

## QUICK COMMAND RECAP (once Node + SDK are sorted)
```
cd Desktop\GODS_ECOSYSTEM\udoc-mobile
npm install
npx cap add android
npx cap sync
npx cap open android
```
…then in Android Studio: **Build → Build APK(s) → locate.**
