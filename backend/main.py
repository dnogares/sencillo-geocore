import asyncio
import json
import uuid
from datetime import datetime
from typing import List
from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from logic.completo import run_cadastral_processing

app = FastAPI(title="GEOCORE API")

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
        success = await run_cadastral_processing(ref, log_callback)
        if not success:
            await log_callback(f"Fallo en la referencia {ref}.", "error")

    await log_callback("Empaquetando resultados en ZIP...", "info")
    await asyncio.sleep(1.5)
    
    await log_callback("PROCESO COMPLETADO EXITOSAMENTE.", "success")

@app.post("/upload")
async def upload_project(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    content = await file.read()
    references = content.decode("utf-8").splitlines()
    references = [r.strip() for r in references if r.strip()]
    
    task_id = str(uuid.uuid4())
    background_tasks.add_task(process_cadastral_task, task_id, file.filename, references)
    
    return {"task_id": task_id, "project_name": file.filename, "ref_count": len(references)}

@app.get("/stream/{task_id}")
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
                    
                    if logs[-1]["message"].endswith("EXITOSAMENTE."):
                        break
            
            await asyncio.sleep(0.5)
            
    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
