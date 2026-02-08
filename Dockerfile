# Usamos una imagen ligera de Node.js
FROM node:20-slim

# Directorio de trabajo
WORKDIR /app

# Copiamos los archivos de configuración primero para aprovechar la caché de Docker
COPY package*.json ./

# Instalamos las dependencias con el flag para ignorar conflictos de versiones de peer dependencies
RUN npm install --legacy-peer-deps && npm install -g serve

# Copiamos el resto del código fuente
COPY . .

# Construimos la aplicación (genera la carpeta /dist)
RUN npm run build

# Exponemos el puerto que usará Easypanel (por defecto suele ser el 3000)
EXPOSE 3000

# Ejecutamos 'serve'. 
# El flag -s permite que las rutas de React funcionen correctamente (Single Page App)
# El flag -l 3000 indica el puerto
CMD ["serve", "-s", "dist", "-l", "3000"]