"""
Chat especialista en GIS usando Gemini Flash 2.0 (gratis)
"""
import os
import json
from pathlib import Path
from typing import List, Dict, Optional
import google.generativeai as genai

# Configuración de la API de Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# System prompt especializado en GIS y Catastro español
SYSTEM_PROMPT = """Eres un experto en Sistemas de Información Geográfica (GIS) y Catastro español.

TU MISIÓN:
- Analizar datos catastrales y cartográficos de España
- Explicar afecciones urbanísticas y ambientales
- Interpretar superficies, coordenadas y geometrías
- Responder preguntas sobre normativa catastral española

CONOCIMIENTOS CLAVE:
- Catastro español: referencias catastrales, polígonos, parcelas
- Afecciones: Red Natura 2000, Montes Públicos, Vías Pecuarias
- Sistemas de coordenadas: EPSG:4326 (WGS84), EPSG:25830 (UTM 30N)
- Normativa: Ley del Suelo, espacios protegidos

ESTILO DE RESPUESTA:
- Conciso y técnico, pero comprensible
- Usa datos específicos del expediente cuando estén disponibles
- Si no tienes información, indícalo claramente
- Proporciona cifras exactas (m², Ha, %)

FORMATO:
- Usa Markdown para estructurar respuestas
- Resalta cifras importantes en **negrita**
- Usa listas cuando enumeres afecciones o datos
"""


class ChatGIS:
    """Gestor del chat especializado en GIS."""
    
    def __init__(self, task_id: str, outputs_root: Path):
        """
        Inicializa el chat para un proyecto específico.
        
        Args:
            task_id: ID del proyecto procesado
            outputs_root: Ruta base de los outputs
        """
        self.task_id = task_id
        self.project_dir = outputs_root / task_id
        
        # Configurar modelo Gemini Flash 2.0 (gratuito)
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            generation_config={
                "temperature": 0.7,
                "top_p": 0.95,
                "max_output_tokens": 2048,
            },
            system_instruction=SYSTEM_PROMPT
        )
        
        # Historial de conversación
        self.chat_session = self.model.start_chat(history=[])
        
        # Cargar contexto del proyecto
        self.context = self._load_project_context()
    
    def _load_project_context(self) -> str:
        """
        Carga y estructura el contexto del proyecto desde los archivos generados.
        
        Returns:
            String con el contexto completo del proyecto
        """
        if not self.project_dir.exists():
            return "⚠️ Proyecto no encontrado. No hay datos disponibles."
        
        context_parts = [
            f"# EXPEDIENTE CATASTRAL: {self.task_id}",
            "\n## ARCHIVOS DISPONIBLES:\n"
        ]
        
        # 1. Leer log.txt (resumen del expediente)
        log_file = self.project_dir / "log.txt"
        if log_file.exists():
            context_parts.append("### LOG DEL EXPEDIENTE:")
            context_parts.append(f"```\n{log_file.read_text(encoding='utf-8')}\n```\n")
        
        # 2. Leer datos catastrales (CSV)
        csv_file = self.project_dir / "DATOS_CATASTRALES.csv"
        if csv_file.exists():
            context_parts.append("### DATOS CATASTRALES (CSV):")
            context_parts.append(f"```csv\n{csv_file.read_text(encoding='utf-8')}\n```\n")
        
        # 3. Leer análisis de afecciones (CSV)
        afecciones_file = self.project_dir / "afecciones_resultados.csv"
        if afecciones_file.exists():
            context_parts.append("### ANÁLISIS DE AFECCIONES:")
            context_parts.append(f"```csv\n{afecciones_file.read_text(encoding='utf-8')}\n```\n")
        
        # 4. Listar planos disponibles
        planos = list(self.project_dir.glob("PLANO-*.jpg"))
        if planos:
            context_parts.append("### PLANOS GENERADOS:")
            for plano in sorted(planos):
                context_parts.append(f"- {plano.name}")
            context_parts.append("")
        
        # 5. Listar archivos XML de parcelas
        xmls = list(self.project_dir.glob("*_INSPIRE.xml"))
        if xmls:
            context_parts.append(f"### PARCELAS PROCESADAS: {len(xmls)}")
            for xml in sorted(xmls):
                ref = xml.stem.replace("_INSPIRE", "")
                context_parts.append(f"- {ref}")
            context_parts.append("")
        
        return "\n".join(context_parts)
    
    async def send_message(self, user_message: str) -> str:
        """
        Envía un mensaje al chat y obtiene la respuesta.
        
        Args:
            user_message: Mensaje del usuario
            
        Returns:
            Respuesta del asistente
        """
        if not GEMINI_API_KEY:
            return (
                "⚠️ **API Key de Gemini no configurada**\n\n"
                "Para usar el chat, configura la variable de entorno `GEMINI_API_KEY`.\n\n"
                "Puedes obtener una clave gratuita en: https://aistudio.google.com/apikey"
            )
        
        try:
            # Primera vez: enviar contexto del proyecto
            if len(self.chat_session.history) == 0:
                context_message = (
                    f"{self.context}\n\n"
                    f"**PREGUNTA DEL USUARIO:**\n{user_message}"
                )
                response = self.chat_session.send_message(context_message)
            else:
                # Conversación normal
                response = self.chat_session.send_message(user_message)
            
            return response.text
            
        except Exception as e:
            return f"❌ Error al comunicar con Gemini: {str(e)}"
    
    def get_history(self) -> List[Dict[str, str]]:
        """
        Obtiene el historial de la conversación.
        
        Returns:
            Lista de mensajes con rol y contenido
        """
        history = []
        for msg in self.chat_session.history:
            history.append({
                "role": msg.role,
                "content": msg.parts[0].text
            })
        return history


# Función helper para crear instancias del chat
def create_chat_session(task_id: str, outputs_root: Path) -> ChatGIS:
    """
    Crea una nueva sesión de chat para un proyecto.
    
    Args:
        task_id: ID del proyecto
        outputs_root: Directorio de outputs
        
    Returns:
        Instancia de ChatGIS
    """
    return ChatGIS(task_id, outputs_root)
