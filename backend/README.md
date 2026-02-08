# Backend GIS Catastral

Este es el backend del sistema de procesamiento GIS catastral.

## 📁 Estructura de Directorios

```
backend/
├── logic/
│   └── completo.py          # Orquestador principal del pipeline GIS (19 pasos)
├── main.py                  # API FastAPI
├── FUENTES/                 # Datos geoespaciales (montado como volumen)
│   ├── CAPAS_gpkg/
│   │   ├── afecciones/      # Capas GPKG para análisis de afecciones
│   │   ├── catastro/        # Datos catastrales locales
│   │   └── sigpac/          # Capas SIGPAC
│   ├── CAPAS_online/        # Referencias a servicios WMS/WFS
│   └── LEYENDAS/            # Imágenes de leyendas para planos
├── outputs/                 # Resultados generados por el procesamiento
└── static/                  # Frontend compilado (React)
```

## 🚀 Configuración de Rutas

El sistema detecta automáticamente el entorno y configura las rutas apropiadas:

### Desarrollo Local (Windows)
```
FUENTES: z:/sencillo/backend/FUENTES
OUTPUTS: z:/sencillo/backend/outputs
```

### Producción (Easypanel/Docker)
```
FUENTES: /app/FUENTES (montado como volumen)
OUTPUTS: /app/outputs
```

## 🔧 Variables de Entorno

- `PYTHONUNBUFFERED=1` - Logs en tiempo real sin buffering

## 📦 Dependencias Principales

- **FastAPI** - Framework web async
- **GeoPandas** - Procesamiento de datos geoespaciales
- **GDAL** - Biblioteca de geoespacial
- **Matplotlib** - Generación de mapas y gráficos
- **Contextily** - Mapas base (OSM, ESRI, etc.)
- **Pandas** - Análisis de datos tabular

## 🛠️ Pipeline de Procesamiento

El orquestador `completo.py` ejecuta 19 pasos organizados en 12 fases:

1. **Adquisición de Datos** - Descarga XML INSPIRE y PDFs del Catastro
2. **Generación Vectorial** - Crea KML y siluetas PNG
3. **Exportación Tabular** - Genera Excel y CSV con datos
4. **Documentación** - Crea log del expediente
5. **Análisis Espacial** - Calcula afecciones con capas GPKG locales
6. **Planos de Emplazamiento** - OSM y ortofoto
7. **Planos Catastrales** - WMS Catastro
8. **Planos IGN Detallados** - Diferentes zoom levels
9. **Planos Provinciales** - Vista regional con diferentes bases
10. **Planos Históricos** - MTN25, MTN50, Catastrones
11. **Planos Temáticos** - Pendientes, Natura 2000
12. **Planos de Protección** - Montes Públicos, Vías Pecuarias

## 🔌 API Endpoints

### `POST /api/upload`
Sube un archivo .txt con referencias catastrales para procesar.

**Request Body:**
```
file: archivo .txt con una referencia catastral por línea
```

**Response:**
```json
{
  "task_id": "uuid-de-la-tarea",
  "project_name": "nombre-archivo.txt",
  "ref_count": 5
}
```

### `GET /api/stream/{task_id}`
Stream de logs en tiempo real del procesamiento (Server-Sent Events).

### `GET /api/download/{task_id}`
Descarga el archivo ZIP con todos los resultados generados.

## 🐳 Docker

### Build Local
```bash
docker build -t geocore-backend .
```

### Run con Docker Compose
```bash
docker-compose up --build
```

### Volúmenes Importantes

En **Easypanel**, configura el volumen:
```
Host Path: /ruta/a/tus/datos/FUENTES
Container Path: /app/FUENTES
```

## 📝 Notas de Desarrollo

1. **FUENTES debe existir**: El directorio FUENTES NO se crea automáticamente. Debe existir y contener las capas GPKG necesarias.

2. **Capas GPKG requeridas**: 
   - Coloca los archivos .gpkg de afecciones en `FUENTES/CAPAS_gpkg/afecciones/`
   - Coloca las vías pecuarias en `FUENTES/CAPAS_gpkg/` (por ejemplo: `RGVP2024.gpkg`)

3. **Procesamiento asíncrono**: 
   - La API usa tareas en background para no bloquear
   - Los logs se transmiten en tiempo real vía SSE (Server-Sent Events)
   - El ZIP se genera al finalizar todas las referencias

4. **Formato de referencias catastrales**:
   - Mínimo 14 caracteres
   - Formato: PPMMMSSSCCPPPP (provincia, municipio, sector, polígono, parcela)
   - Ejemplo: `28079A01900001`

## 🆘 Troubleshooting

### Error: "No se encontró FUENTES_DIR"
- Verifica que el volumen está montado correctamente
- En desarrollo: verifica que existe `z:/sencillo/backend/FUENTES`
- En producción: verifica la configuración del volumen en Easypanel

### Error: "No hay capas de afecciones"
- Verifica que existen archivos .gpkg en `FUENTES/CAPAS_gpkg/afecciones/`
- Los archivos deben tener extensión `.gpkg`

### Error en generación de planos
- Verifica conectividad a internet (necesario para servicios WMS)
- Algunos servicios externos pueden fallar temporalmente (IGN, Catastro, etc.)

## 🔗 Servicios Externos Utilizados

- **Catastro INSPIRE WFS**: Geometrías catastrales oficiales
- **Sede Catastro**: PDFs de croquis y datos gráficos
- **OpenStreetMap**: Mapas base
- **ESRI ArcGIS**: Mapas topográficos y callejeros
- **IGN**: Mapas topográficos históricos (MTN25, MTN50)
- **MITECO**: Servicios WFS de Montes Públicos
