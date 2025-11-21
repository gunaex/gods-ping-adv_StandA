import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        timeout: 60000
      },
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true,
        changeOrigin: true,
        secure: false,
        rewriteWsOrigin: true,
        timeout: 60000,
        // Handle WebSocket proxy errors gracefully
        configure: (proxy, options) => {
          proxy.on('error', (err, req, res) => {
            console.log('WebSocket proxy error:', err.message);
          });
          proxy.on('proxyReqWs', (proxyReq, req, socket) => {
            console.log('WebSocket proxy request:', req.url);
          });
        }
      }
    }
  }
})
