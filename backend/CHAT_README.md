# 🤖 Chat Especialista en GIS

Sistema de chat basado en **Gemini Flash 2.0** (gratuito) que analiza los datos generados por el pipeline catastral.

## ✨ Capacidades

El chat puede:
- 📊 **Analizar datos catastrales**: superficies, coordenadas, polígonos
- 🌍 **Interpretar afecciones**: Red Natura 2000, Montes Públicos, Vías Pecuarias
- 📝 **Resumir expedientes**: estadísticas, totales, superficies
- 🗺️ **Explicar planos**: qué representa cada mapa generado
- ⚖️ **Asesorar sobre normativa**: Ley del Suelo, espacios protegidos

## 🔧 Configuración

### 1. Obtener API Key de Gemini (GRATIS)

1. Ve a: https://aistudio.google.com/apikey
2. Inicia sesión con tu cuenta de Google
3. Haz clic en "Create API Key"
4. Copia la clave generada

### 2. Configurar en Easypanel

1. Ve al servicio `backend` en Easypanel
2. Pestaña **Environment**
3. Añade la variable:
   - **Nombre**: `GEMINI_API_KEY`
   - **Valor**: [tu_api_key_copiada]
4. **Guarda** y **Redeploy**

### 3. Configurar en Local (Docker Compose)

Crea un archivo `.env` en la raíz del proyecto:

```bash
GEMINI_API_KEY=tu_api_key_aqui
```

Modifica `docker-compose.yml` para cargar el `.env`:

```yaml
backend:
  env_file:
    - .env
```

## 📡 Endpoints de la API

### POST `/api/chat/{task_id}`

Envía un mensaje al chat para analizar un proyecto específico.

**Request:**
```json
{
  "message": "¿Qué porcentaje del terreno está afectado por Red Natura 2000?"
}
```

**Response:**
```json
{
  "response": "Según el análisis de afecciones...",
  "task_id": "abc123"
}
```

### GET `/api/chat/{task_id}/history`

Obtiene el historial completo de la conversación.

**Response:**
```json
{
  "history": [
    {"role": "user", "content": "..."},
    {"role": "model", "content": "..."}
  ]
}
```

### DELETE `/api/chat/{task_id}`

Elimina la sesión de chat (libera memoria).

**Response:**
```json
{
  "message": "Sesión de chat eliminada"
}
```

## 💡 Ejemplos de Preguntas

- "Resume el expediente catastral"
- "¿Cuántas parcelas se han procesado?"
- "¿Qué afecciones tiene el terreno?"
- "Explica qué es Red Natura 2000"
- "¿Cuál es la superficie total en hectáreas?"
- "¿Hay montes de utilidad pública?"
- "Resume las coordenadas del centroide"

## 🧠 Contexto que Recibe el Chat

Cuando inicias una conversación, el chat carga automáticamente:

1. **log.txt** - Resumen del expediente
2. **DATOS_CATASTRALES.csv** - Tabla con referencias, polígonos, parcelas
3. **afecciones_resultados.csv** - Análisis de intersecciones
4. **Lista de planos** - PLANO-*.jpg generados
5. **Referencias procesadas** - Archivos XML disponibles

## 🚀 Límites y Rendimiento

- **Modelo**: Gemini Flash 2.0 Experimental
- **Costo**: 100% gratuito
- **Límites**: ~60 requests/minuto (tier gratuito)
- **Respuesta**: ~2-5 segundos por mensaje
- **Contexto**: Hasta 2048 tokens de salida

## 🔐 Seguridad

- La API Key se configura como variable de entorno
- **NUNCA** subas el `.env` al repositorio
- El `.env` ya está en `.gitignore`
- Las sesiones de chat se almacenan en memoria (no persisten)

## 🐛 Troubleshooting

### "API Key de Gemini no configurada"

**Solución**: Configura `GEMINI_API_KEY` en las variables de entorno de Easypanel.

### "Error 429: Quota exceeded"

**Solución**: Espera 1 minuto. El tier gratuito tiene límite de ~60 req/min.

### "Proyecto no encontrado"

**Solución**: Verifica que el `task_id` exista en `/outputs/`.

---

## 📚 Más Información

- [Documentación de Gemini API](https://ai.google.dev/docs)
- [Obtener API Key](https://aistudio.google.com/apikey)
- [Límites del Tier Gratuito](https://ai.google.dev/pricing)
