import asyncio
import json
import uuid
import shutil
import os
from datetime import datetime
from typing import List
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from logic.completo import run_cadastral_processing

app = FastAPI(title="GEOCORE API")

# Directorios de trabajo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUTS_ROOT = os.path.join(BASE_DIR, "outputs")

# Detectar entorno y configurar ruta de FUENTES
# En Easypanel (producción): /app/FUENTES (montado como volumen)
# En local (desarrollo): z:/sencillo/backend/FUENTES o relativo a BASE_DIR
if os.path.exists("/app/FUENTES"):
    # Entorno de producción (Easypanel)
    FUENTES_DIR = "/app/FUENTES"
    print("🚀 Entorno de producción detectado: usando /app/FUENTES")
elif os.path.exists("z:/sencillo/backend/FUENTES"):
    # Entorno de desarrollo local (Windows, unidad Z:)
    FUENTES_DIR = "z:/sencillo/backend/FUENTES"
    print("💻 Entorno de desarrollo detectado: usando z:/sencillo/backend/FUENTES")
else:
    # Fallback: usar ruta relativa al directorio del script
    FUENTES_DIR = os.path.join(BASE_DIR, "FUENTES")
    print(f"⚠️  Usando ruta fallback: {FUENTES_DIR}")

os.makedirs(OUTPUTS_ROOT, exist_ok=True)
# FUENTES_DIR no se crea, el volumen debe existir y estar montado
print(f"📁 FUENTES_DIR: {FUENTES_DIR}")
print(f"📂 OUTPUTS_ROOT: {OUTPUTS_ROOT}")


# Configurar CORS para el frontend de React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Almacén temporal de logs (en producción usaríamos Redis o una DB)
task_logs = {}

def get_timestamp():
    return datetime.now().strftime("%H:%M:%S")

async def process_cadastral_task(task_id: str, project_name: str, references: List[str]):
    task_logs[task_id] = []
    task_dir = os.path.join(OUTPUTS_ROOT, task_id)
    os.makedirs(task_dir, exist_ok=True)
    
    async def log_callback(message, log_type="info"):
        log_entry = {
            "id": str(uuid.uuid4()),
            "timestamp": get_timestamp(),
            "message": f"[{project_name}] {message}",
            "type": log_type
        }
        task_logs[task_id].append(log_entry)

    await log_callback(f"Iniciando procesamiento de {len(references)} referencias.", "info")
    
    for ref in references:
        # Ahora pasamos el directorio de fuentes para que la lógica lo use
        success = await run_cadastral_processing(ref, log_callback, task_dir, FUENTES_DIR)
        if not success:
            await log_callback(f"Fallo en la referencia {ref}.", "error")

    await log_callback("Empaquetando resultados en ZIP...", "info")
    
    # Verificar si hay archivos para comprimir
    files_in_dir = os.listdir(task_dir)
    await log_callback(f"Archivos encontrados para comprimir: {len(files_in_dir)}", "info")
    
    # Crear el archivo ZIP
    zip_base_name = os.path.join(OUTPUTS_ROOT, f"resultados_{task_id}")
    shutil.make_archive(zip_base_name, 'zip', task_dir)
    
    zip_full_path = f"{zip_base_name}.zip"
    if os.path.exists(zip_full_path):
        size_kb = os.path.getsize(zip_full_path) / 1024
        await log_callback(f"ZIP creado exitosamente ({size_kb:.1f} KB).", "success")
    else:
        await log_callback("ERROR: No se pudo crear el archivo ZIP.", "error")
    
    download_url = f"/api/download/{task_id}"
    await log_callback(f"PROCESO COMPLETADO EXITOSAMENTE. URL:{download_url}", "success")

@app.post("/api/upload")
async def upload_project(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    content = await file.read()
    references = content.decode("utf-8").splitlines()
    references = [r.strip() for r in references if r.strip()]
    
    task_id = str(uuid.uuid4())
    background_tasks.add_task(process_cadastral_task, task_id, file.filename, references)
    
    return {"task_id": task_id, "project_name": file.filename, "ref_count": len(references)}

@app.get("/api/stream/{task_id}")
async def stream_logs(task_id: str):
    async def event_generator():
        sent_count = 0
        while True:
            if task_id in task_logs:
                logs = task_logs[task_id]
                if len(logs) > sent_count:
                    for i in range(sent_count, len(logs)):
                        yield f"data: {json.dumps(logs[i])}\n\n"
                    sent_count = len(logs)
                    
                    if logs[-1]["message"].endswith("EXITOSAMENTE.") or "URL:" in logs[-1]["message"]:
                        break
            
            await asyncio.sleep(0.5)
            
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/api/download/{task_id}")
async def download_results(task_id: str):
    zip_path = os.path.join(OUTPUTS_ROOT, f"resultados_{task_id}.zip")
    if not os.path.exists(zip_path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    
    return FileResponse(
        zip_path, 
        media_type="application/zip", 
        filename=f"resultados_{task_id}.zip"
    )

# Servir archivos estáticos del frontend
if os.path.exists("static"):
    app.mount("/assets", StaticFiles(directory="static/assets"), name="assets")

    @app.get("/")
    async def serve_index():
        return FileResponse("static/index.html")

    @app.get("/{rest_of_path:path}")
    async def serve_frontend(rest_of_path: str):
        # Si no es una ruta de API, intentamos servir el index para el routing de React
        if not rest_of_path.startswith("api/"):
            return FileResponse("static/index.html")
        raise HTTPException(status_code=404)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
