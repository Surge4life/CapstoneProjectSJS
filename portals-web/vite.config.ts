import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { VitePWA } from "vite-plugin-pwa";
export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: "autoUpdate",
      manifest: {
        name: "G.O.D.S Ecosystem Portals",
        short_name: "G.O.D.S",
        description: "Student, Employer & Employee portals for the G.O.D.S ecosystem",
        theme_color: "#060E1C",
        background_color: "#060E1C",
        display: "standalone",
        icons: [
          { src: "icon-192.png", sizes: "192x192", type: "image/png" },
          { src: "icon-512.png", sizes: "512x512", type: "image/png" }
        ]
      }
    })
  ],
});
