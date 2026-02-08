# Etapa 1: Construcción
FROM node:20-slim as build
WORKDIR /app
COPY package*.json ./
RUN npm install --legacy-peer-deps
COPY . .
RUN npm run build

# Etapa 2: Servidor de producción (Nginx)
FROM nginx:alpine
# Copiamos los archivos compilados
COPY --from=build /app/dist /usr/share/nginx/html
# Copiamos nuestra configuración de proxy
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]