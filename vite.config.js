import { defineConfig } from "vite";
import path from "path";

export default defineConfig({
  build: {
    outDir: "./static",
    emptyOutDir: false,
    manifest: true,
    rollupOptions: {
      input: "src/js/main.js",
    },
  },
  server: {
    host: "0.0.0.0",
    port: 5173,
  },
});
