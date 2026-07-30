const { app, BrowserWindow, shell, Menu } = require("electron");
const path = require("path");

// INTERNAL UDOC Desktop — staff / UDOC admins / GODS internal only.
// Client SaaS desktop is a separate package: udoc-desktop-client.
const ADMIN_URL =
  process.env.UDOC_ADMIN_URL ||
  process.env.GODS_URL ||
  "https://gods-udoc-admin.onrender.com";
const SENTINEL_URL =
  process.env.UDOC_SENTINEL_URL ||
  "https://gods-platform-core.onrender.com/Sentinel";
const PORTALS_URL =
  process.env.UDOC_PORTALS_URL ||
  "https://gods-platform-core.onrender.com/portals";
const CORE_ADMIN_URL =
  process.env.UDOC_CORE_ADMIN_URL ||
  "https://gods-platform-core.onrender.com/admin";

function createWindow(startUrl) {
  const win = new BrowserWindow({
    width: 1280,
    height: 860,
    title: "UDOC Internal · GODS Staff",
    icon: path.join(__dirname, "icon.png"),
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  win.setMenuBarVisibility(true);
  win.loadURL(startUrl || ADMIN_URL);

  win.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: "deny" };
  });

  win.webContents.on("did-fail-load", () => {
    win.loadURL(
      "data:text/html;charset=utf-8," +
        encodeURIComponent(
          "<body style='background:#060E1C;color:#C9A84C;font-family:sans-serif;display:flex;" +
            "align-items:center;justify-content:center;height:100vh;text-align:center;padding:24px'>" +
            "<div><h1>UDOC Internal</h1>" +
            "<p style='color:#D0C8B0'>Could not reach Admin host.</p>" +
            "<p style='color:#8A9BB0;font-size:.9rem'>Free tier may be waking. Wait ~30s and reopen.<br>" +
            "Staff-only · not client SaaS · set UDOC_ADMIN_URL to override.</p></div></body>"
        )
    );
  });

  return win;
}

function buildMenu() {
  const template = [
    {
      label: "UDOC Internal",
      submenu: [
        {
          label: "Admin console",
          click: () => {
            const w = BrowserWindow.getFocusedWindow();
            if (w) w.loadURL(ADMIN_URL);
          },
        },
        {
          label: "Sentinel EVA",
          click: () => {
            const w = BrowserWindow.getFocusedWindow();
            if (w) w.loadURL(SENTINEL_URL);
          },
        },
        {
          label: "24 Portals dual-path",
          click: () => {
            const w = BrowserWindow.getFocusedWindow();
            if (w) w.loadURL(PORTALS_URL);
          },
        },
        {
          label: "Core constitutional /admin",
          click: () => {
            const w = BrowserWindow.getFocusedWindow();
            if (w) w.loadURL(CORE_ADMIN_URL);
          },
        },
        { type: "separator" },
        { role: "reload" },
        { role: "quit" },
      ],
    },
  ];
  Menu.setApplicationMenu(Menu.buildFromTemplate(template));
}

app.whenReady().then(() => {
  buildMenu();
  createWindow(ADMIN_URL);
});
app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});
app.on("activate", () => {
  if (BrowserWindow.getAllWindows().length === 0) createWindow(ADMIN_URL);
});
