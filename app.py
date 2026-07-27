"""
Interfaz web del Portal de Soporte BimBam Buy.
"""
import streamlit as st
from src.agente import AgenteBimBam
from src.indexador import ejecutar_indexacion
import os

# --- Configuración de la página ---
st.set_page_config(
    page_title="Portal de Soporte | BimBam Buy",
    page_icon="💼",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- CSS Corporativo Sobrio ---
st.markdown("""
<style>
    /* Estilos base */
    html, body, [class*="css"] {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .stApp { 
        background-color: #f4f6f9;
    }
    
    /* Contenedor central */
    .main .block-container {
        padding: 2rem !important;
        max-width: 800px !important;
        background-color: white;
        box-shadow: 0 0 10px rgba(0,0,0,0.05);
        border-radius: 8px;
        margin-top: 2rem;
    }
    
    /* Títulos */
    h1 {
        color: #0056b3 !important;
        font-size: 2.2rem !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    .subtitle {
        color: #666;
        font-size: 1rem;
        margin-bottom: 20px;
    }
    
    /* Globos de Chat Estándar */
    .stChatMessage {
        border-radius: 4px;
        padding: 1rem;
        margin-bottom: 1rem;
        border: 1px solid #e0e0e0;
    }
    
    /* Usuario */
    [data-testid="stChatMessage"]:nth-child(even) {
        background-color: #f8f9fa;
        border-left: 4px solid #6c757d;
    }
    
    /* Sistema (Agente) */
    [data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #ffffff;
        border-left: 4px solid #0056b3;
    }
    
    /* Ajustes visuales para Markdown */
    .stMarkdown p { font-size: 0.95rem; color: #333; line-height: 1.5; }
    
</style>
""", unsafe_allow_html=True)

# --- Encabezado ---
st.markdown("<h1>Portal de Soporte Interno</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>BimBam Buy - Base de Conocimiento Operativa</p>", unsafe_allow_html=True)

# --- Inicialización del Sistema ---
@st.cache_resource(show_spinner="Cargando base de datos documental...")
def inicializar_sistema():
    if not os.path.exists("chroma_db"):
        st.info("Inicializando repositorio de documentos. Por favor espere...")
        ejecutar_indexacion()
    return AgenteBimBam()

agente = inicializar_sistema()

# --- Gestión del Historial de Chat ---
if "mensajes" not in st.session_state:
    st.session_state.mensajes = [
        {
            "role": "assistant", 
            "content": "Bienvenido al sistema de consulta de políticas operativas. Puede ingresar su consulta respecto a Envíos, Garantías, Reembolsos, Pagos o Afiliados en la caja de texto inferior.",
            "avatar": "🏢"
        }
    ]

# Mostrar los mensajes anteriores (sin fuentes)
for mensaje in st.session_state.mensajes:
    avatar = mensaje.get("avatar", "👤" if mensaje["role"] == "user" else "🏢")
    with st.chat_message(mensaje["role"], avatar=avatar):
        st.markdown(mensaje["content"])

# --- Entrada de Usuario ---
pregunta_usuario = st.chat_input("Ingrese su consulta...")

if pregunta_usuario:
    # 1. Mostrar la pregunta del usuario
    st.session_state.mensajes.append({"role": "user", "content": pregunta_usuario, "avatar": "👤"})
    with st.chat_message("user", avatar="👤"):
        st.markdown(pregunta_usuario)
    
    # 2. Generar y mostrar la respuesta
    with st.chat_message("assistant", avatar="🏢"):
        with st.spinner("Buscando en los registros..."):
            resultado = agente.preguntar(pregunta_usuario)
            
            # Solo extraemos la respuesta, ignoramos las fuentes
            respuesta_texto = resultado["respuesta"]
            
            st.markdown(respuesta_texto)
            
    # 3. Guardar en historial
    st.session_state.mensajes.append({
        "role": "assistant", 
        "content": respuesta_texto,
        "avatar": "🏢"
    })

# --- Barra Lateral (Sidebar) ---
with st.sidebar:
    st.markdown("### 🏢 Panel de Opciones")
    st.markdown("""
    Sistema de consulta interna.
    Uso exclusivo para colaboradores de BimBam Buy.
    """)
    
    st.divider()
    
    st.markdown("#### Módulos Activos:")
    st.caption("■ Tiempos y Costos de Envío")
    st.caption("■ Manual de Garantía")
    st.caption("■ Reembolsos y Devoluciones")
    st.caption("■ Métodos de Pago")
    st.caption("■ Programa de Afiliados")
    
    st.divider()
    
    if st.button("Limpiar Sesión", type="secondary", use_container_width=True):
        st.session_state.mensajes = [
            {"role": "assistant", "content": "Sesión reiniciada. Ingrese una nueva consulta.", "avatar": "🏢"}
        ]
        agente.reiniciar_conversacion()
        st.rerun()
