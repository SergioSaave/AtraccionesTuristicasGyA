import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',  // Asegúrate de que el servidor escuche en 0.0.0.0
    port: 5173,       // Puedes especificar el puerto que deseas utilizar
  },
})