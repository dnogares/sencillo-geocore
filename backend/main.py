import asyncio
import json
import uuid
import shutil
import os
from datetime import datetime
from typing import List
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
from logic.completo import run_cadastral_processing
from logic.chat_gis import create_chat_session

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
    """
    Procesa un conjunto de referencias catastrales de forma asíncrona.
    """
    print(f"\n{'='*80}")
    print(f"[TASK {task_id}] Iniciando procesamiento de {project_name}")
    print(f"[TASK {task_id}] Referencias: {len(references)}")
    print(f"{'='*80}\n")
    
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
        # Debug: Verificar que se está guardando
        print(f"[LOG_CALLBACK] Task {task_id}: guardado log #{len(task_logs[task_id])} - {message[:50]}")
        # También imprimir en stdout para los logs de Easypanel
        print(f"[{log_type.upper()}] {message}")

    await log_callback(f"Iniciando procesamiento de {len(references)} referencias.", "info")
    
    for ref in references:
        print(f"[TASK {task_id}] Procesando referencia: {ref}")
        # Ahora pasamos el directorio de fuentes para que la lógica lo use
        try:
            success = await run_cadastral_processing(ref, log_callback, task_dir, FUENTES_DIR)
            if not success:
                await log_callback(f"Fallo en la referencia {ref}.", "error")
        except Exception as e:
            await log_callback(f"Error procesando {ref}: {str(e)}", "error")
            print(f"[ERROR] Excepción en {ref}: {e}")
            import traceback
            traceback.print_exc()

    await log_callback("Empaquetando resultados en ZIP...", "info")
    
    # Verificar si hay archivos para comprimir
    files_in_dir = os.listdir(task_dir)
    await log_callback(f"Archivos encontrados para comprimir: {len(files_in_dir)}", "info")
    print(f"[TASK {task_id}] Archivos en {task_dir}: {files_in_dir[:10]}")  # Mostrar primeros 10
    
    # Crear el archivo ZIP
    zip_base_name = os.path.join(OUTPUTS_ROOT, f"resultados_{task_id}")
    shutil.make_archive(zip_base_name, 'zip', task_dir)
    
    zip_full_path = f"{zip_base_name}.zip"
    if os.path.exists(zip_full_path):
        size_kb = os.path.getsize(zip_full_path) / 1024
        await log_callback(f"ZIP creado exitosamente ({size_kb:.1f} KB).", "success")
        print(f"[TASK {task_id}] ZIP creado: {zip_full_path} ({size_kb:.1f} KB)")
    else:
        await log_callback("ERROR: No se pudo crear el archivo ZIP.", "error")
        print(f"[ERROR TASK {task_id}] No se pudo crear el ZIP")
    
    download_url = f"/api/download/{task_id}"
    await log_callback(f"PROCESO COMPLETADO EXITOSAMENTE. URL:{download_url}", "success")
    print(f"[TASK {task_id}] PROCESO FINALIZADO\n")

@app.post("/api/upload")
async def upload_project(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    content = await file.read()
    references = content.decode("utf-8").splitlines()
    references = [r.strip() for r in references if r.strip()]
    
    task_id = str(uuid.uuid4())
    
    print(f"\n{'='*80}")
    print(f"[UPLOAD] Nuevo proyecto subido: {file.filename}")
    print(f"[UPLOAD] Task ID: {task_id}")
    print(f"[UPLOAD] Referencias: {len(references)}")
    print(f"{'='*80}\n")
    
    background_tasks.add_task(process_cadastral_task, task_id, file.filename, references)
    
    return {"task_id": task_id, "project_name": file.filename, "ref_count": len(references)}

# Estado de las tareas (en memoria)
task_status = {}  # {task_id: {"status": "processing"|"completed"|"error", "download_url": "...", "error": "..."}}

@app.post("/api/process-async")
async def process_async(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    """
    Inicia procesamiento en background y devuelve task_id inmediatamente.
    El cliente debe hacer polling a /api/status/{task_id} para ver el progreso.
    """
    try:
        content = await file.read()
        references = content.decode("utf-8").splitlines()
        references = [r.strip() for r in references if r.strip()]
        
        task_id = str(uuid.uuid4())
        
        # Inicializar estado
        task_status[task_id] = {
            "status": "processing",
            "filename": file.filename,
            "ref_count": len(references)
        }
        
        print(f"\n{'='*80}")
        print(f"[ASYNC] Inicio para: {file.filename}")
        print(f"[ASYNC] Task ID: {task_id}")
        print(f"[ASYNC] Referencias: {len(references)}")
        print(f"{'='*80}\n")
        
        # Función wrapper que actualiza el estado al finalizar
        async def process_and_update_status():
            try:
                await process_cadastral_task(task_id, file.filename, references)
                
                # Verificar que el ZIP se creó
                zip_path = os.path.join(OUTPUTS_ROOT, f"resultados_{task_id}.zip")
                if os.path.exists(zip_path):
                    file_size_kb = os.path.getsize(zip_path) / 1024
                    task_status[task_id] = {
                        "status": "completed",
                        "download_url": f"/api/download/{task_id}",
                        "file_size": f"{file_size_kb:.1f} KB"
                    }
                    print(f"[ASYNC] ✅ Task {task_id} completado\n")
                else:
                    task_status[task_id] = {
                        "status": "error",
                        "error": "ZIP no generado"
                    }
            except Exception as e:
                task_status[task_id] = {
                    "status": "error",
                    "error": str(e)
                }
                print(f"[ASYNC] ❌ Task {task_id} error: {e}\n")
        
        background_tasks.add_task(process_and_update_status)
        
        return {
            "success": True,
            "task_id": task_id,
            "message": "Procesamiento iniciado"
        }
        
    except Exception as e:
        print(f"[ASYNC] ❌ Error al iniciar: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.get("/api/status/{task_id}")
async def get_status(task_id: str):
    """
    Devuelve el estado actual de un task (respuesta instantánea, sin timeout).
    """
    if task_id not in task_status:
        return JSONResponse(
            status_code=404,
            content={"status": "notfound", "error": "Task no encontrado"}
        )
    
    return task_status[task_id]

@app.get("/api/debug/{task_id}")
async def debug_task(task_id: str):
    """
    Endpoint de debugging para ver el estado de los logs.
    """
    return {
        "task_exists": task_id in task_logs,
        "log_count": len(task_logs.get(task_id, [])),
        "all_tasks": list(task_logs.keys()),
        "sample_logs": task_logs.get(task_id, [])[:5] if task_id in task_logs else []
    }

@app.get("/api/logs/{task_id}")
async def get_logs(task_id: str):
    """
    Endpoint de polling para obtener logs (reemplaza SSE problemático).
    """
    print(f"[API /logs/{task_id}] Petición recibida. Task exists: {task_id in task_logs}")
    
    if task_id not in task_logs:
        print(f"[API /logs/{task_id}] Task NO encontrado en task_logs")
        return JSONResponse(content={
            "logs": [],
            "completed": False,
            "message": "Task no encontrado o aún no iniciado"
        })
    
    logs = task_logs[task_id]
    completed = False
    
    print(f"[API /logs/{task_id}] Devolviendo {len(logs)} logs")
    
    # Verificar si el proceso ha terminado
    if logs:
        last_msg = logs[-1]["message"]
        if ("COMPLETADO" in last_msg.upper() and "URL:" in last_msg) or \
           ("PROCESO COMPLETADO" in last_msg.upper()):
            completed = True
    
    return JSONResponse(content={
        "logs": logs,
        "completed": completed
    })

# Mantener endpoint SSE legacy por compatibilidad
@app.get("/api/stream/{task_id}")
async def stream_logs(task_id: str):
    """
    Endpoint de Server-Sent Events para streaming de logs en tiempo real.
    DEPRECADO: Usar /api/logs/{task_id} con polling en su lugar.
    """
    print(f"[STREAM] Cliente conectado para task: {task_id}")
    
    async def event_generator():
        sent_count = 0
        iterations = 0
        max_iterations = 600  # 5 minutos máximo (600 * 0.5s)
        
        while iterations < max_iterations:
            iterations += 1
            
            if task_id in task_logs:
                logs = task_logs[task_id]
                if len(logs) > sent_count:
                    # Enviar nuevos logs
                    for i in range(sent_count, len(logs)):
                        yield f"data: {json.dumps(logs[i])}\n\n"
                    sent_count = len(logs)
                    
                    # Detectar finalización (buscar "COMPLETADO" o "URL:" en el último mensaje)
                    if logs:
                        last_msg = logs[-1]["message"]
                        if ("COMPLETADO" in last_msg.upper() and "URL:" in last_msg) or \
                           ("PROCESO COMPLETADO" in last_msg.upper()):
                            print(f"[STREAM] Proceso {task_id} finalizado detectado")
                            break
            elif iterations == 1:
                # Primera iteración: verificar si el task existe
                print(f"[STREAM] Task {task_id} aún no tiene logs (esperando...)")
            
            await asyncio.sleep(0.5)
        
        # Log final si se alcanzó el timeout
        if iterations >= max_iterations:
            print(f"[STREAM] Timeout alcanzado para task {task_id}")
            
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

# ═══════════════════════════════════════════════════════════════════════════
# ENDPOINTS DE CHAT GIS (GEMINI)
# ═══════════════════════════════════════════════════════════════════════════

# Modelo de petición de chat
class ChatMessage(BaseModel):
    message: str

# Almacenamiento de sesiones de chat (en memoria)
chat_sessions = {}

@app.post("/api/chat/{task_id}")
async def chat_with_gis(task_id: str, chat_msg: ChatMessage):
    """
    Endpoint de chat especializado en GIS para analizar un proyecto.
    
    Args:
        task_id: ID del proyecto procesado
        chat_msg: Mensaje del usuario
        
    Returns:
        JSON con la respuesta del asistente
    """
    try:
        # Verificar que el proyecto existe
        task_dir = Path(OUTPUTS_ROOT) / task_id
        if not task_dir.exists():
            raise HTTPException(status_code=404, detail="Proyecto no encontrado")
        
        # Crear o recuperar sesión de chat
        if task_id not in chat_sessions:
            chat_sessions[task_id] = create_chat_session(task_id, Path(OUTPUTS_ROOT))
        
        chat = chat_sessions[task_id]
        
        # Enviar mensaje y obtener respuesta
        response = await chat.send_message(chat_msg.message)
        
        return JSONResponse(content={
            "response": response,
            "task_id": task_id
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el chat: {str(e)}")

@app.get("/api/chat/{task_id}/history")
async def get_chat_history(task_id: str):
    """
    Obtiene el historial de conversación de un proyecto.
    
    Args:
        task_id: ID del proyecto
        
    Returns:
        JSON con el historial completo
    """
    if task_id not in chat_sessions:
        return JSONResponse(content={"history": []})
    
    chat = chat_sessions[task_id]
    history = chat.get_history()
    
    return JSONResponse(content={"history": history})

@app.delete("/api/chat/{task_id}")
async def clear_chat_session(task_id: str):
    """
    Limpia la sesión de chat de un proyecto.
    
    Args:
        task_id: ID del proyecto
        
    Returns:
        JSON confirmando la limpieza
    """
    if task_id in chat_sessions:
        del chat_sessions[task_id]
    
    return JSONResponse(content={"message": "Sesión de chat eliminada"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
