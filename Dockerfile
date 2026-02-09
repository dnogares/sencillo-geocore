# ============================================
# DOCKERFILE OPTIMIZADO - Multi-stage Build
# ============================================

# --- STAGE 1: Builder ---
FROM node:20-slim AS builder

WORKDIR /app

# Copiar solo archivos de dependencias primero (cache layer)
COPY package*.json ./

# Instalar dependencias con optimizaciones
RUN npm ci --only=production --ignore-scripts && \
    npm cache clean --force

# Copiar código fuente
COPY . .

# Build de producción con optimizaciones
ENV NODE_ENV=production
RUN npm run build

# --- STAGE 2: Runtime ---
FROM node:20-slim AS runtime

WORKDIR /app

# Instalar solo el servidor estático (sin devDependencies)
RUN npm install -g serve@14 && \
    npm cache clean --force

# Copiar solo los archivos buildeados desde el stage anterior
COPY --from=builder /app/dist ./dist

# Crear usuario non-root para seguridad
RUN useradd -m -u 1001 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Exponer puerto
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000', (r) => r.statusCode === 200 ? process.exit(0) : process.exit(1))"

# Comando optimizado con configuración de cache
CMD ["serve", "-s", "dist", "-l", "3000", "-a", "0.0.0.0", "--no-clipboard", "-c", "serve.json"]
