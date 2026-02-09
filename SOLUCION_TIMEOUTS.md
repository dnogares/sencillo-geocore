# 🚨 Solución a Errores HTTP 524/502 - Timeouts del Servidor

## 📋 Problema Identificado

```
HTTP 524: Timeout del proxy Cloudflare/Easypanel (>100s sin respuesta)
HTTP 502: Bad Gateway (backend FastAPI caído o no responde)
```

**Causa**: El procesamiento catastral tarda varios minutos (5-10min con múltiples referencias) pero el proxy tiene timeout de ~100 segundos.

---

## ✅ Solución Inmediata (5 minutos)

### **Cambiar a ProcessorSimple.tsx**

Este componente usa el enfoque correcto para procesos largos:

**Paso 1: Editar `src/App.tsx`**

```tsx
// CAMBIAR ESTA LÍNEA:
import { Processor } from './components/Processor';

// POR ESTA:
import { ProcessorSimple as Processor } from './components/ProcessorSimple';
```

**Paso 2: Rebuild y redeploy**

```bash
git add src/App.tsx
git commit -m "fix: usar ProcessorSimple para evitar timeouts HTTP 524/502"
git push origin main
```

**Paso 3: Rebuild en Easypanel**

El deploy automático debería activarse.

---

## 🔍 Diferencias Clave

| Aspecto | Processor.tsx (Actual) | ProcessorSimple.tsx (Solución) |
|---------|------------------------|--------------------------------|
| **Endpoint inicial** | `/api/upload` | `/api/process-async` |
| **Polling** | `/api/logs/{id}` cada 3s | `/api/status/{id}` cada 2s |
| **Datos transferidos** | Todos los logs (pesado) | Solo status (ligero) |
| **Logs en UI** | Terminal en tiempo real | Incluidos en ZIP final |
| **Timeout risk** | Alto (mucho tráfico) | Bajo (mínimo tráfico) |
| **Robustez** | Media | Alta |

---

## 📁 Ubicación de Archivos en Servidor

```
/app/backend/OUTPUTS/
├── [task_id]/
│   ├── XML, PDF, KML, PNG...
│   ├── PLANO-*.jpg (19 planos)
│   ├── log.txt  ← Logs incluidos aquí
│   └── ...
└── resultados_[task_id].zip  ← Archivo final para descarga
```

**Endpoint de descarga**: `GET /api/download/{task_id}`

---

## 🎯 Arquitectura Correcta para Procesos Largos

### **Flujo Actual (Problemas)**
```
Frontend → POST /upload → Backend empieza a procesar
Frontend → GET /logs/{id} cada 3s (polling pesado)
          ↓
     ❌ TIMEOUT después de 100s
```

### **Flujo Correcto (ProcessorSimple)**
```
Frontend → POST /process-async → Backend responde INMEDIATAMENTE
                                  Background task empieza
Frontend → GET /status/{id} cada 2s (solo: "processing"|"completed"|"error")
          ↓
     ✅ Respuestas instantáneas, NO timeout
     ✅ Cuando status="completed" → mostrar botón descarga
```

---

## ⚙️ Configuración Adicional en Easypanel (Opcional)

Si quieres mantener Processor.tsx con logs en tiempo real, necesitas:

### **1. Aumentar timeouts en nginx**

```nginx
# En configuración de tu servicio en Easypanel
proxy_read_timeout 600;
proxy_connect_timeout 600;
proxy_send_timeout 600;
```

### **2. Aumentar timeout de Uvicorn**

```python
# En backend/main.py al final
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        timeout_keep_alive=600  # 10 minutos
    )
```

### **3. Configurar variables de entorno en Easypanel**

```env
UVICORN_TIMEOUT_KEEP_ALIVE=600
UVICORN_TIMEOUT_GRACEFUL_SHUTDOWN=30
```

**PERO**: Esto solo parchea el problema, no lo resuelve. ProcessorSimple es la solución correcta.

---

## 📊 Comparación de Rendimiento

### **Con Processor.tsx (polling de logs)**
```
Peticiones HTTP por proyecto de 3 refs (5 min proceso):
- 1x POST /upload
- 100x GET /logs/{id} (cada 3s × 100 = 300s)
= 101 peticiones HTTP

Tráfico de datos:
- Logs completos × 100 = ~500KB transferidos
- RIESGO: Timeout si proxy < 300s
```

### **Con ProcessorSimple.tsx (polling de status)**
```
Peticiones HTTP por proyecto de 3 refs (5 min proceso):
- 1x POST /process-async
- 150x GET /status/{id} (cada 2s × 150 = 300s)
= 151 peticiones HTTP

Tráfico de datos:
- Solo JSON status × 150 = ~15KB transferidos
- SIN RIESGO: Respuestas instantáneas (<100ms)
```

---

## 🚀 Acción Recomendada

**AHORA MISMO:**
1. Cambiar import en `App.tsx` a `ProcessorSimple`
2. Commit y push
3. Esperar deploy automático en Easypanel

**FUTURO (mejora adicional):**
1. Implementar WebSocket para logs en tiempo real
2. O usar Redis Pub/Sub para streaming
3. O implementar Server-Sent Events sin proxy

---

## 📝 Notas Técnicas

### ¿Por qué falla el polling de logs?

```python
# En main.py, endpoint /api/logs/{task_id}
# Cada request devuelve TODO el array de logs
# Si hay 500 logs × 100 bytes = 50KB por request
# × 100 requests = 5MB transferidos

# Problema: response time puede ser lento
# si hay muchos logs, causando timeout del proxy
```

### ¿Por qué funciona el polling de status?

```python
# En main.py, endpoint /api/status/{task_id}
# Solo devuelve: {"status": "processing"}
# ~50 bytes por request
# Response time: <10ms (instantáneo)
# ✅ Proxy nunca hace timeout
```

---

## ✅ Verificación Post-Deploy

Después de cambiar a ProcessorSimple, deberías ver en la consola:

```javascript
[ASYNC] Task iniciado: abc-123
[STATUS] Estado: processing
[STATUS] Estado: processing
...
[STATUS] Estado: completed
✅ Archivo disponible para descarga
```

**Sin errores HTTP 524/502** ✨

---

**Creado**: 2026-02-09  
**Prioridad**: 🔴 CRÍTICA  
**Tiempo estimado**: 5 minutos para fix
