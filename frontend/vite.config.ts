import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from "path";

export default defineConfig({
  plugins: [vue()],
  server: {
    host: true, 
    port: 5173,
  },
  build: {
    outDir: path.resolve(__dirname, "dist"), 
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
  },
});