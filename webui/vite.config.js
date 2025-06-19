import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';

export default defineConfig({
  plugins: [
    react(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['favicon.svg'],
      manifest: {
        name: 'PiWardrive Web',
        short_name: 'PiWardrive',
        start_url: '/',
        display: 'standalone',
        background_color: '#ffffff',
        icons: [
          {
            src: 'favicon.svg',
            sizes: 'any',
            type: 'image/svg+xml'
          }
        ]
      }
    })
  ],
  server: {
    proxy: {
      '/status': 'http://localhost:8000',
      '/widget-metrics': 'http://localhost:8000',
      '/logs': 'http://localhost:8000',
      '/config': 'http://localhost:8000',
      '/plugins': 'http://localhost:8000',
      '/api/widgets': 'http://localhost:8000',
      '/dashboard-settings': 'http://localhost:8000',
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true
      }
    }
  }
});
