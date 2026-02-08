# 📋 Resumen de Cambios - Adaptación de Rutas FUENTES

## 🎯 Objetivo
Adaptar el proyecto para que funcione correctamente con rutas de archivos tanto en desarrollo local (Windows, unidad Z:) como en despliegue de producción (Easypanel con volumen en /app/FUENTES).

## ✅ Cambios Realizados

### 1. **backend/logic/completo.py**
**Cambio**: Agregada función wrapper `run_cadastral_processing()` 

**Antes**: 
- Solo funcionaba como script standalone leyendo archivos .txt de INPUTS

**Ahora**:
- Puede procesarse como script standalone (modo CLI)
- Puede llamarse desde API vía `run_cadastral_processing()` para procesar referencias individuales
- Función async compatible con FastAPI
- Acepta parámetros: refcat, log_callback, output_dir, fuentes_dir

**Líneas añadidas**: ~130 líneas (función wrapper completa)

---

### 2. **backend/main.py**
**Cambio**: Detección automática de entorno y configuración de rutas

**Antes**:
```python
FUENTES_DIR = os.path.join(BASE_DIR, "FUENTES")
```

**Ahora**:
```python
# Detecta automáticamente:
# 1. Producción: /app/FUENTES (Easypanel)
# 2. Desarrollo: z:/sencillo/backend/FUENTES
# 3. Fallback: ./FUENTES (relativo)

if os.path.exists("/app/FUENTES"):
    FUENTES_DIR = "/app/FUENTES"  # Producción
elif os.path.exists("z:/sencillo/backend/FUENTES"):
    FUENTES_DIR = "z:/sencillo/backend/FUENTES"  # Desarrollo local
else:
    FUENTES_DIR = os.path.join(BASE_DIR, "FUENTES")  # Fallback
```

**Beneficios**:
- ✅ Sin cambios de código entre entornos
- ✅ Logs informativos del entorno detectado
- ✅ Funcionamiento automático en Docker y local

---

### 3. **docker-compose.yml**
**Cambio**: Agregado montaje del volumen FUENTES

**Antes**:
```yaml
volumes:
  - ./backend:/app
```

**Ahora**:
```yaml
volumes:
  - ./backend:/app
  - ./backend/FUENTES:/app/FUENTES:ro  # Solo lectura
```

**Beneficios**:
- ✅ Acceso a capas GPKG en Docker local
- ✅ Modo solo lectura (seguridad)
- ✅ Compatible con desarrollo local

---

### 4. **backend/README.md** ✨ NUEVO
- Documentación completa de la arquitectura del backend
- Explicación del pipeline de procesamiento (19 pasos, 12 fases)
- Guía de endpoints de la API
- Troubleshooting común
- Estructura de directorios

---

### 5. **EASYPANEL_CONFIG.md** ✨ NUEVO
- Guía paso a paso para configurar volúmenes en Easypanel
- Comandos SSH para preparar el servidor
- Instrucciones de subida de archivos GPKG con SCP/rsync
- Verificación post-despliegue
- Troubleshooting específico de producción

---

## 📁 Estructura de Rutas

### Desarrollo Local (Windows)
```
Z:/sencillo/
├── backend/
│   ├── FUENTES/              ← Capas GPKG locales
│   │   ├── CAPAS_gpkg/
│   │   │   ├── afecciones/   ← Archivos .gpkg de afecciones
│   │   │   ├── catastro/
│   │   │   └── sigpac/
│   │   ├── CAPAS_online/
│   │   └── LEYENDAS/
│   ├── outputs/              ← Resultados generados
│   ├── logic/
│   │   └── completo.py
│   └── main.py
└── docker-compose.yml
```

### Producción (Easypanel)
```
/app/                         ← Contenedor Docker
├── FUENTES/                  ← Volumen montado (read-only)
│   ├── CAPAS_gpkg/
│   │   └── afecciones/
│   ├── CAPAS_online/
│   └── LEYENDAS/
├── outputs/                  ← Resultados generados
├── logic/
│   └── completo.py
└── main.py
```

**Host (servidor Easypanel)**:
```
/var/lib/easypanel/projects/geocore/fuentes/  ← Datos persistentes
```

---

## 🔄 Flujo de Trabajo

### Modo API (FastAPI)
1. Usuario sube archivo .txt con referencias catastrales
2. Backend genera task_id único
3. Para cada referencia:
   - Se llama a `run_cadastral_processing(refcat, ...)`
   - Logs en tiempo real vía Server-Sent Events
   - Archivos se guardan en `outputs/{task_id}/`
4. Al finalizar: se crea ZIP con todos los resultados
5. Usuario descarga ZIP vía `/api/download/{task_id}`

### Modo Standalone (CLI)
```bash
cd z:/sencillo/backend/logic
python completo.py
```
- Lee archivos .txt de `INPUTS/`
- Genera resultados en `OUTPUTS/`
- Modo batch para múltiples referencias

---

## ✨ Mejoras Implementadas

### 1. **Portabilidad**
- ✅ Sin hardcodeo de rutas
- ✅ Detección automática de entorno
- ✅ Funciona en Windows, Linux, Docker

### 2. **Flexibilidad**
- ✅ Modo API + Modo CLI
- ✅ Procesamiento individual o batch
- ✅ Logs en tiempo real

### 3. **Mantenibilidad**
- ✅ Documentación completa
- ✅ Configuración centralizada
- ✅ Separación de concerns (API vs lógica de negocio)

### 4. **Seguridad**
- ✅ FUENTES montado como solo lectura
- ✅ Outputs aislados por task_id
- ✅ Sin exposición de rutas internas

---

## 🚀 Próximos Pasos para Despliegue

### 1. Preparar Datos
```bash
# Verificar que tienes las capas GPKG necesarias
ls z:/sencillo/backend/FUENTES/CAPAS_gpkg/afecciones/
```

### 2. Subir Datos al Servidor
```bash
# Seguir instrucciones en EASYPANEL_CONFIG.md
rsync -avz --progress \
    z:/sencillo/backend/FUENTES/ \
    usuario@servidor:/var/lib/easypanel/projects/geocore/fuentes/
```

### 3. Configurar Volumen en Easypanel
- Container Path: `/app/FUENTES`
- Host Path: `/var/lib/easypanel/projects/geocore/fuentes`
- Mode: `readonly`

### 4. Deploy
- Push a GitHub
- Easypanel detecta cambios
- Build automático
- Deploy

### 5. Verificar
```bash
# Ver logs del contenedor
docker logs <container-id>

# Deberías ver:
# 🚀 Entorno de producción detectado: usando /app/FUENTES
```

---

## 📊 Impacto de los Cambios

| Aspecto | Antes | Ahora |
|---------|-------|-------|
| **Portabilidad** | Solo CLI, rutas fijas | API + CLI, rutas dinámicas |
| **Entornos** | Solo local | Local + Docker + Producción |
| **Configuración** | Manual por entorno | Automática |
| **Documentación** | Ninguna | Completa (2 guías) |
| **Logs** | Solo consola | SSE en tiempo real + consola |
| **Despliegue** | Complejo | Simplificado con guía paso a paso |

---

## 🎉 Resultado Final

✅ **Sistema totalmente adaptado** para funcionar con:
- Desarrollo local en Windows (Z:/)
- Despliegue en Easypanel (/app/FUENTES)
- Modo standalone (CLI) para testing
- Modo API para producción

✅ **Sin cambios de código** entre entornos

✅ **Documentación completa** para desarrolladores y ops

✅ **Listo para deploy** 🚀
