import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
// Internal console: in production this is served ONLY on the internal network and points at
// platform-core's internal bind. Dev proxies to localhost for convenience.
export default defineConfig({
  plugins: [react()],
  server: { proxy: { "/api": { target: "http://localhost:8000", changeOrigin: true, rewrite: p => p.replace(/^\/api/, "") } } },
});
