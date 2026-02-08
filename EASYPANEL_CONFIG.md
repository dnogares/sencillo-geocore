# Configuración de Easypanel para GeoCore

## 📋 Configuración del Servicio

### Variables de Entorno
```
PYTHONUNBUFFERED=1
```

### Puertos
- **Puerto del contenedor**: 8000
- **Puerto público**: 80 (o el que prefieras)

### Comando de Inicio
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 📁 Configuración de Volúmenes

### Volumen FUENTES (CRÍTICO)

Este volumen contiene todas las capas geoespaciales necesarias para el análisis.

**Configuración en Easypanel:**

```
Name: fuentes-gis
Host Path: /var/lib/easypanel/projects/geocore/fuentes
Container Path: /app/FUENTES
Mode: read-only (ro)
```

**Estructura requerida en el host:**

```
/var/lib/easypanel/projects/geocore/fuentes/
├── CAPAS_gpkg/
│   ├── afecciones/
│   │   ├── espacios_protegidos.gpkg
│   │   ├── dominio_publico_hidraulico.gpkg
│   │   ├── red_natura_2000.gpkg
│   │   ├── montes_utilidad_publica.gpkg
│   │   └── ... (otros archivos .gpkg)
│   ├── catastro/
│   │   └── (opcional: capas catastrales locales)
│   └── sigpac/
│       └── (opcional: capas SIGPAC locales)
├── CAPAS_online/
│   └── (archivos de configuración de servicios WMS/WFS)
└── LEYENDAS/
    └── (imágenes PNG de leyendas para los planos)
```

### Volumen OUTPUTS (Opcional)

Para persistir los resultados entre reinicios:

```
Name: outputs-gis
Host Path: /var/lib/easypanel/projects/geocore/outputs
Container Path: /app/outputs
Mode: read-write (rw)
```

## 🚀 Pasos de Despliegue

### 1. Preparar el Servidor

Conéctate al servidor donde está Easypanel:

```bash
ssh usuario@tu-servidor.com
```

### 2. Crear Estructura de Directorios

```bash
# Crear directorio base del proyecto
sudo mkdir -p /var/lib/easypanel/projects/geocore

# Crear estructura de FUENTES
sudo mkdir -p /var/lib/easypanel/projects/geocore/fuentes/CAPAS_gpkg/afecciones
sudo mkdir -p /var/lib/easypanel/projects/geocore/fuentes/CAPAS_gpkg/catastro
sudo mkdir -p /var/lib/easypanel/projects/geocore/fuentes/CAPAS_gpkg/sigpac
sudo mkdir -p /var/lib/easypanel/projects/geocore/fuentes/CAPAS_online
sudo mkdir -p /var/lib/easypanel/projects/geocore/fuentes/LEYENDAS

# Crear directorio de outputs
sudo mkdir -p /var/lib/easypanel/projects/geocore/outputs
```

### 3. Subir Archivos GPKG

Desde tu máquina local, sube los archivos .gpkg al servidor:

```bash
# Usando SCP
scp z:/sencillo/backend/FUENTES/CAPAS_gpkg/afecciones/*.gpkg \
    usuario@servidor:/var/lib/easypanel/projects/geocore/fuentes/CAPAS_gpkg/afecciones/

# O usando rsync (mejor para múltiples archivos)
rsync -avz --progress \
    z:/sencillo/backend/FUENTES/ \
    usuario@servidor:/var/lib/easypanel/projects/geocore/fuentes/
```

### 4. Verificar Permisos

```bash
# Dar permisos apropiados
sudo chown -R 1000:1000 /var/lib/easypanel/projects/geocore/fuentes
sudo chmod -R 755 /var/lib/easypanel/projects/geocore/fuentes
```

### 5. Configurar en Easypanel

1. Ve a **Easypanel Dashboard**
2. Crea o edita tu servicio "geocore-backend"
3. En la sección **Volumes**, agrega:
   - **Volume 1**: 
     - Container Path: `/app/FUENTES`
     - Host Path: `/var/lib/easypanel/projects/geocore/fuentes`
     - Mode: `readonly`
   - **Volume 2** (opcional):
     - Container Path: `/app/outputs`
     - Host Path: `/var/lib/easypanel/projects/geocore/outputs`
     - Mode: `readwrite`

### 6. Build & Deploy

1. Conecta tu repositorio de GitHub
2. Configura el **Build Context**: `./`
3. Configura el **Dockerfile Path**: `./backend/Dockerfile`
4. Haz Deploy

## 🔍 Verificación Post-Despliegue

### Comprobar que FUENTES está montado

```bash
# Entrar al contenedor
docker exec -it <container-id> /bin/bash

# Verificar que existe el directorio
ls -la /app/FUENTES

# Verificar que hay archivos GPKG
ls -la /app/FUENTES/CAPAS_gpkg/afecciones/
```

### Comprobar logs del backend

```bash
docker logs <container-id> -f
```

Deberías ver:
```
🚀 Entorno de producción detectado: usando /app/FUENTES
📁 FUENTES_DIR: /app/FUENTES
📂 OUTPUTS_ROOT: /app/outputs
```

## ⚠️ Consideraciones Importantes

### Tamaño de los Archivos GPKG

Los archivos GPKG pueden ser muy grandes (varios GB). Considera:

1. **Espacio en disco**: Verifica que tienes suficiente espacio en el servidor
2. **Compresión**: Comprime los archivos antes de subirlos (si GDAL lo soporta)
3. **Backup**: Mantén copias de seguridad de estos archivos

### Actualizaciones de Datos

Para actualizar las capas GPKG en producción:

```bash
# 1. Subir nuevo archivo
scp nuevo_archivo.gpkg usuario@servidor:/tmp/

# 2. Mover al directorio correcto
ssh usuario@servidor
sudo mv /tmp/nuevo_archivo.gpkg \
    /var/lib/easypanel/projects/geocore/fuentes/CAPAS_gpkg/afecciones/

# 3. Ajustar permisos
sudo chown 1000:1000 /var/lib/easypanel/projects/geocore/fuentes/CAPAS_gpkg/afecciones/nuevo_archivo.gpkg

# 4. Reiniciar el contenedor (opcional, solo si es necesario)
# El sistema debe detectar automáticamente el nuevo archivo
```

## 🐛 Troubleshooting

### Error: "Access denied - path outside allowed directories"

El contenedor no puede acceder a `/app/FUENTES`. Verifica:
- Que el volumen está correctamente configurado en Easypanel
- Que el directorio del host existe y tiene permisos correctos

### Error: "No hay capas de afecciones en FUENTES/CAPAS_gpkg/afecciones"

- Verifica que los archivos .gpkg están en la ruta correcta del host
- Verifica que el volumen está montado en `/app/FUENTES` (no en `/app/backend/FUENTES`)

### Performance lento

- Los archivos GPKG grandes pueden ralentizar el procesamiento
- Considera usar índices espaciales en los archivos GPKG
- Verifica la RAM disponible en el servidor

## 📞 Soporte

Para más información, consulta:
- README.md del backend
- Documentación de GeoPandas: https://geopandas.org/
- Documentación de GDAL: https://gdal.org/
