"""
Configuración centralizada del proyecto Agente BimBam Buy.
Todas las constantes y parámetros se definen aquí.
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# ─── Rutas del proyecto ───────────────────────────────────────────
DIRECTORIO_BASE = os.path.dirname(os.path.dirname(__file__))
DIRECTORIO_DATOS = os.path.join(DIRECTORIO_BASE, "data")
DIRECTORIO_CHROMA = os.path.join(DIRECTORIO_BASE, "chroma_db")

# ─── Configuración de Chunking ────────────────────────────────────
TAMANO_CHUNK = 500       # Caracteres por chunk
SOLAPAMIENTO_CHUNK = 100 # Solapamiento entre chunks para no perder contexto

# ─── Configuración de OpenAI ──────────────────────────────────────
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODELO_EMBEDDINGS = "text-embedding-3-small"  # Modelo de embeddings de OpenAI (económico)
MODELO_LLM = "gpt-4o-mini"                   # Modelo de chat (económico y potente)
TEMPERATURA_LLM = 0.2                         # Baja temperatura = respuestas más precisas

# ─── Configuración de Recuperación ─────────────────────────────────
TOP_K = 5  # Número de fragmentos a recuperar por consulta
