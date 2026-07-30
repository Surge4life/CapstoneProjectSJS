const { app, BrowserWindow, shell, Menu } = require("electron");
const path = require("path");

// CLIENT UDOC Desktop — tenant SaaS only (models, govern, reports, policy view).
// Staff/admin desktop is udoc-desktop/ (Internal).
const CLIENT_URL =
  process.env.UDOC_CLIENT_URL || "https://gods-udoc-client.onrender.com";
const SAAS_PORTALS_URL =
  process.env.UDOC_SAAS_PORTALS_URL || "https://gods-udoc-portals.onrender.com";
const SECTOR_URL =
  process.env.UDOC_SECTOR_URL || "https://gods-udoc-sector.onrender.com";
const CITIZEN_URL =
  process.env.UDOC_CITIZEN_URL ||
  "https://gods-udoc-client.onrender.com/citizen.html";

function createWindow(startUrl) {
  const win = new BrowserWindow({
    width: 1280,
    height: 860,
    title: "UDOC Client · Tenant SaaS",
    icon: path.join(__dirname, "icon.png"),
    webPreferences: {
      preload: path.join(__dirname, "preload.js"),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  win.setMenuBarVisibility(true);
  win.loadURL(startUrl || CLIENT_URL);

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
            "<div><h1>UDOC Client</h1>" +
            "<p style='color:#D0C8B0'>Could not reach Client host.</p>" +
            "<p style='color:#8A9BB0;font-size:.9rem'>Tenant SaaS only · set UDOC_CLIENT_URL to override.</p></div></body>"
        )
    );
  });

  return win;
}

function buildMenu() {
  const template = [
    {
      label: "UDOC Client",
      submenu: [
        {
          label: "Governance console",
          click: () => {
            const w = BrowserWindow.getFocusedWindow();
            if (w) w.loadURL(CLIENT_URL);
          },
        },
        {
          label: "SaaS Portals",
          click: () => {
            const w = BrowserWindow.getFocusedWindow();
            if (w) w.loadURL(SAAS_PORTALS_URL);
          },
        },
        {
          label: "Sector console",
          click: () => {
            const w = BrowserWindow.getFocusedWindow();
            if (w) w.loadURL(SECTOR_URL);
          },
        },
        {
          label: "Citizen (public)",
          click: () => {
            const w = BrowserWindow.getFocusedWindow();
            if (w) w.loadURL(CITIZEN_URL);
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
  createWindow(CLIENT_URL);
});
app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});
app.on("activate", () => {
  if (BrowserWindow.getAllWindows().length === 0) createWindow(CLIENT_URL);
});
