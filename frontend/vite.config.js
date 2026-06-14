import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    proxy: {
      '/api': {
        // Local dev: backend runs on :8001 (8000 is taken by another project).
        // Docker prod uses nginx.conf instead of this proxy.
        target: 'http://localhost:8001',
        changeOrigin: true,
      }
    }
  }
})