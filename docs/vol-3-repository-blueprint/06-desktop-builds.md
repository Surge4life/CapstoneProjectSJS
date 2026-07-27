# Chapter 06 — Desktop Builds

## Overview

Each division app has a desktop build directory (`{division}-desktop/`). Desktop builds package the web app as a native desktop application using Electron or Tauri, enabling distribution as a `.exe` (Windows), `.dmg` (macOS), or `.AppImage` (Linux).

---

## Why Desktop Builds?

Some G.O.D.S deployment contexts require a desktop application:
- **Enterprise environments** where browser-based apps are restricted by IT policy
- **Air-gapped deployments** where the app must be distributed as an offline installer
- **Compliance officers** who prefer a dedicated application with native OS integration (system tray, notifications, file system access)
- **Offline-capable administration** for deployment contexts with intermittent connectivity

---

## Directory Structure

```
{division}-desktop/
├── src/
│   ├── main.js          Main process (Electron entry point)
│   ├── preload.js       Preload script (contextBridge)
│   └── config.js        Default configuration
├── build/               Build assets (icons for Windows/macOS/Linux)
├── package.json
├── electron-builder.yml Distribution configuration
└── README.md
```

---

## Electron Configuration

```javascript
// src/main.js (simplified)
const { app, BrowserWindow, ipcMain } = require('electron');

function createWindow() {
  const win = new BrowserWindow({
    width: 1280,
    height: 800,
    titleBarStyle: 'hiddenInset',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,    // Security: no direct Node access from renderer
    },
    icon: path.join(__dirname, '../build/icon.png'),
    backgroundColor: '#060E1C',  // G.O.D.S navy (shown before page loads)
  });

  // Load the built web app
  win.loadFile(path.join(__dirname, '../../{division}-app/dist/index.html'));
}

app.whenReady().then(createWindow);
```

---

## Distribution Targets

```yaml
# electron-builder.yml
appId: com.gods.seths.desktop
productName: SETHS Desktop
copyright: "Copyright 2025 Sashin J. Singh / G.O.D.S Holdings (Pty) Ltd (proposed)"

directories:
  buildResources: build

win:
  target: nsis          # Windows installer
  icon: build/icon.ico

mac:
  target: dmg           # macOS disk image
  icon: build/icon.icns

linux:
  target: AppImage      # Linux portable app
  icon: build/icon.png
```

---

## Security Model for Desktop Apps

Desktop apps run with elevated trust compared to browser apps. Security constraints:

1. **`contextIsolation: true`** — renderer process (web content) cannot directly access Node.js APIs
2. **`nodeIntegration: false`** — web content cannot use `require()`
3. **`contextBridge`** — the only way for web content to communicate with the main process is via explicitly exposed APIs
4. **Content Security Policy** — strict CSP applied to the loaded web content
5. **No remote URL loading** — the app loads local files only; API calls go to the configured backend URL

```javascript
// preload.js — the security boundary
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
  getBackendUrl: () => ipcRenderer.invoke('get-backend-url'),
  setBackendUrl: (url) => ipcRenderer.invoke('set-backend-url', url),
  openExternal: (url) => ipcRenderer.invoke('open-external', url),
  // Only expose what the web app actually needs
});
```

---

## The Connect Screen in Desktop

Like the mobile apps, desktop apps show a connect screen to configure the backend URL. The URL is persisted in Electron's `app.getPath('userData')` — not in the repository, not in a browser cookie.

This means a desktop app installation on an enterprise laptop can be configured once to point at the enterprise's private G.O.D.S deployment, and the configuration persists across app updates.
