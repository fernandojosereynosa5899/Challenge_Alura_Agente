"""
Interfaz web del Agente BimBam Buy.
Estilo: TRUE LIQUID CRYSTAL (Animado, Holográfico, Glassmorphism Extremo)
"""
import streamlit as st
from src.agente import AgenteBimBam
from src.indexador import ejecutar_indexacion
import os

st.set_page_config(
    page_title="BimBam Buy | IA",
    page_icon="💎",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- CSS TRUE LIQUID CRYSTAL ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif !important;
        color: #1a1a2e !important;
    }
    
    /* Fondo Fluido Animado (True Liquid Holographic) */
    .stApp { 
        background: linear-gradient(125deg, #a1c4fd 0%, #c2e9fb 25%, #e0c3fc 50%, #8ec5fc 75%, #ffb199 100%);
        background-size: 400% 400%;
        animation: liquidFlow 15s ease infinite;
        background-attachment: fixed;
    }
    
    @keyframes liquidFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Contenedor central ajustado */
    .main .block-container {
        padding: 3rem 1.5rem !important;
        max-width: 850px !important;
    }
    
    /* Título Cromado/Cristalino */
    h1 {
        background: linear-gradient(180deg, #ffffff 0%, #f0f0f0 40%, #cccccc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        font-size: 4rem !important;
        text-align: center;
        letter-spacing: -2px;
        margin-bottom: 0px;
        filter: drop-shadow(0px 4px 8px rgba(0, 0, 0, 0.15));
    }
    
    .subtitle {
        text-align: center;
        color: #ffffff;
        font-weight: 600;
        font-size: 1.4rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 3rem;
        text-shadow: 0 2px 10px rgba(255,255,255,0.5);
    }
    
    /* GLOBOS DE CHAT - EFECTO CRISTAL PURO */
    .stChatMessage {
        border-radius: 24px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        
        /* Glassmorphism Hiper-Realista */
        background: rgba(255, 255, 255, 0.25) !important;
        backdrop-filter: blur(25px) saturate(150%) contrast(120%) !important;
        -webkit-backdrop-filter: blur(25px) saturate(150%) contrast(120%) !important;
        
        /* Reflejos de cristal (Bordes superior e izquierdo más brillantes) */
        border-top: 1px solid rgba(255, 255, 255, 0.8) !important;
        border-left: 1px solid rgba(255, 255, 255, 0.6) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.2) !important;
        
        /* Sombra interior y exterior para profundidad 3D */
        box-shadow: 
            0 12px 32px 0 rgba(31, 38, 135, 0.15),
            inset 0 0 20px rgba(255, 255, 255, 0.5) !important;
        
        animation: levitateIn 0.6s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
    }
    
    /* Distinción Bot vs Usuario con tonalidades sutiles */
    [data-testid="stChatMessage"]:nth-child(odd) {
        background: rgba(240, 248, 255, 0.35) !important; /* Ligeramente azul para bot */
    }
    [data-testid="stChatMessage"]:nth-child(even) {
        background: rgba(255, 240, 245, 0.35) !important; /* Ligeramente rosa/cálido para user */
        text-align: right;
    }
    
    @keyframes levitateIn {
        from { opacity: 0; transform: translateY(30px) scale(0.95); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }
    
    /* INPUT DE CHAT - BARRA DE CRISTAL */
    [data-testid="stChatInput"] {
        border-radius: 40px !important;
        background: rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(30px) saturate(200%) !important;
        -webkit-backdrop-filter: blur(30px) saturate(200%) !important;
        
        border-top: 1px solid rgba(255, 255, 255, 0.9) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.2) !important;
        
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1) !important;
        padding: 0.5rem 1.5rem !important;
        transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
    }
    
    [data-testid="stChatInput"]:focus-within {
        background: rgba(255, 255, 255, 0.6) !important;
        box-shadow: 0 20px 40px rgba(255, 255, 255, 0.3), 0 0 20px rgba(255, 255, 255, 0.5) !important;
        transform: translateY(-4px) scale(1.02);
    }
    
    /* Ajuste de Texto */
    .stMarkdown p { 
        font-size: 1.1rem; 
        color: #1a1a2e; 
        line-height: 1.6;
        text-shadow: 0 1px 2px rgba(255,255,255,0.8); /* Hace legible el texto oscuro sobre cristal */
    }
    
    /* Sidebar también en modo Cristal */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(25px) !important;
        -webkit-backdrop-filter: blur(25px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.5) !important;
    }
    
</style>
""", unsafe_allow_html=True)

# --- Encabezado ---
st.markdown("<h1>BimBam Buy AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>L I Q U I D &nbsp; C R Y S T A L</p>", unsafe_allow_html=True)

# --- Inicialización del Sistema ---
@st.cache_resource(show_spinner="Cristalizando núcleo de datos...")
def inicializar_sistema():
    if not os.path.exists("chroma_db"):
        st.info("Inicializando núcleo de datos...")
        ejecutar_indexacion()
    return AgenteBimBam()

agente = inicializar_sistema()

# --- Gestión del Historial de Chat ---
if "mensajes" not in st.session_state:
    st.session_state.mensajes = [
        {
            "role": "assistant", 
            "content": "¡Hola! 👋 Bienvenido a la inteligencia operativa de BimBam Buy.\n\nEstoy listo para resolver tus dudas sobre **Envíos, Garantías, Reembolsos, Pagos o el Programa de Afiliados**.\n\n¿En qué te ayudo hoy?",
            "avatar": "💎"
        }
    ]

# Mostrar los mensajes
for mensaje in st.session_state.mensajes:
    avatar = mensaje.get("avatar", "👤" if mensaje["role"] == "user" else "💎")
    with st.chat_message(mensaje["role"], avatar=avatar):
        st.markdown(mensaje["content"])

# --- Entrada de Usuario ---
pregunta_usuario = st.chat_input("Toca el cristal para escribir...")

if pregunta_usuario:
    st.session_state.mensajes.append({"role": "user", "content": pregunta_usuario, "avatar": "👤"})
    with st.chat_message("user", avatar="👤"):
        st.markdown(pregunta_usuario)
    
    with st.chat_message("assistant", avatar="💎"):
        with st.spinner("Sintetizando información..."):
            resultado = agente.preguntar(pregunta_usuario)
            respuesta_texto = resultado["respuesta"]
            st.markdown(respuesta_texto)
            
    st.session_state.mensajes.append({
        "role": "assistant", 
        "content": respuesta_texto,
        "avatar": "💎"
    })

# --- Barra Lateral ---
with st.sidebar:
    st.markdown("### 🎛️ Centro de Control")
    st.markdown("""
    Desarrollado con arquitectura **RAG**.
    """)
    st.divider()
    st.markdown("#### 📚 Documentos Base:")
    st.caption("💎 Tiempos y Costos de Envío")
    st.caption("💎 Manual de Garantía")
    st.caption("💎 Reembolsos y Devoluciones")
    st.caption("💎 Métodos de Pago")
    st.caption("💎 Programa de Afiliados")
    st.divider()
    
    if st.button("💫 Limpiar Cristal (Reiniciar)", type="primary", use_container_width=True):
        st.session_state.mensajes = [
            {"role": "assistant", "content": "Cristal limpio. ¡Comenzamos de nuevo! 💎", "avatar": "💎"}
        ]
        agente.reiniciar_conversacion()
        st.rerun()
