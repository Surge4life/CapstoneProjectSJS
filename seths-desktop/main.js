const { app, BrowserWindow, shell } = require("electron");
const path = require("path");

// The G.O.D.S deployment this desktop app connects to. Change to your own URL if different.
const APP_URL = process.env.GODS_URL || "https://gods-portals.onrender.com";

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 820,
    title: "SETHS",
    icon: path.join(__dirname, "icon.png"),
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  win.setMenuBarVisibility(false);
  win.loadURL(APP_URL);

  // External links open in the user's real browser, not inside the app
  win.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: "deny" };
  });

  // If the deployment is asleep/unreachable, show a friendly message
  win.webContents.on("did-fail-load", () => {
    win.loadURL("data:text/html;charset=utf-8," + encodeURIComponent(
      "<body style='background:#060E1C;color:#C9A84C;font-family:sans-serif;display:flex;" +
      "align-items:center;justify-content:center;height:100vh;text-align:center'>" +
      "<div><h1>SETHS</h1><p style='color:#D0C8B0'>Could not reach the G.O.D.S deployment.</p>" +
      "<p style='color:#D0C8B0;font-size:.9rem'>It may be waking up (free tier sleeps after 15 min). " +
      "Wait ~30s and reopen, or check your connection.</p></div></body>"
    ));
  });
}

app.whenReady().then(createWindow);
app.on("window-all-closed", () => { if (process.platform !== "darwin") app.quit(); });
app.on("activate", () => { if (BrowserWindow.getAllWindows().length === 0) createWindow(); });
