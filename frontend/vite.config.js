import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { visualizer } from 'rollup-plugin-visualizer';

export default defineConfig({
  plugins: [
    react(),
    visualizer({
      open: true, // Automatically opens the visualizer after build
      filename: './dist/stats.html', // Output file for visualization
    }),
  ],
  optimizeDeps: {
    include: ['react-router-dom'],
  },
  build: {
    outDir: 'dist',
    minify: 'esbuild',
  },
  resolve: {
    alias: {
      '@': '/src',
    },
  },
});
