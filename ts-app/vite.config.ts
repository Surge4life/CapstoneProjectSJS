import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { VitePWA } from "vite-plugin-pwa";
export default defineConfig({
  plugins: [react(), VitePWA({ registerType: "autoUpdate", manifest: {
    name: "TS Industries · G.O.D.S", short_name: "TS Industries",
    theme_color: "#060E1C", background_color: "#060E1C", display: "standalone",
    icons: [{ src: "icon-192.png", sizes: "192x192", type: "image/png" },
            { src: "icon-512.png", sizes: "512x512", type: "image/png" }] } })],
});
