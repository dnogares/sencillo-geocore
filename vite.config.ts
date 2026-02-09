import path from 'path';
import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig(({ mode }) => {
    const env = loadEnv(mode, '.', '');
    
    return {
      server: {
        port: 3000,
        host: '0.0.0.0',
      },
      
      plugins: [
        react({
          // Optimización: Fast Refresh más eficiente
          fastRefresh: true,
          // Babel optimizations
          babel: {
            plugins: [
              // Remove console.log en producción
              mode === 'production' && 'transform-remove-console'
            ].filter(Boolean)
          }
        })
      ],
      
      // ✅ CRÍTICO: NO exponer API keys en el bundle
      // En su lugar, usar variables de entorno del servidor o proxy
      define: mode === 'production' ? {} : {
        'process.env.API_KEY': JSON.stringify(env.GEMINI_API_KEY),
        'process.env.GEMINI_API_KEY': JSON.stringify(env.GEMINI_API_KEY)
      },
      
      resolve: {
        alias: {
          '@': path.resolve(__dirname, '.'),
        }
      },
      
      build: {
        // Optimizaciones de build
        target: 'es2020',
        minify: 'terser',
        terserOptions: {
          compress: {
            drop_console: true,
            drop_debugger: true,
            pure_funcs: ['console.log', 'console.info']
          }
        },
        
        // Code splitting optimizado
        rollupOptions: {
          output: {
            manualChunks: {
              'react-vendor': ['react', 'react-dom'],
              'icons': ['lucide-react']
            }
          }
        },
        
        // Chunk size warnings
        chunkSizeWarningLimit: 500,
        
        // Source maps solo en desarrollo
        sourcemap: mode !== 'production',
        
        // Optimizar CSS
        cssCodeSplit: true,
        cssMinify: true
      },
      
      // Optimización de dependencias
      optimizeDeps: {
        include: ['react', 'react-dom', 'lucide-react'],
        exclude: []
      }
    };
});
