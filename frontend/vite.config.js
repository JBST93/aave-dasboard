import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
      '@mui/styles': '@mui/styles',
    },
  },
  build: {
    outDir: 'build',
    rollupOptions: {
      external: ['@mui/styles'],
    },
  },
});
