"""
Interfaz web del Agente BimBam Buy.
Estilo: NEO LIQUID CRYSTAL (Futurista, Dark Neon, Tipografías Sci-Fi)
"""
import streamlit as st
from src.agente import AgenteBimBam
from src.indexador import ejecutar_indexacion
import os

st.set_page_config(
    page_title="BimBam Buy | NEON",
    page_icon="🌌",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- CSS NEO LIQUID CRYSTAL ---
st.markdown("""
<style>
    /* Tipografías Futuristas */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Space+Grotesk:wght@300;400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif !important;
        color: #E0E0FF !important;
    }
    
    h1, h2, h3, .subtitle {
        font-family: 'Orbitron', sans-serif !important;
    }
    
    /* Fondo Fluido Oscuro de Neón */
    .stApp { 
        background: linear-gradient(-45deg, #0f0c29, #302b63, #0b8793, #360033);
        background-size: 400% 400%;
        animation: neonLiquid 12s ease infinite;
        background-attachment: fixed;
    }
    
    @keyframes neonLiquid {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Contenedor central */
    .main .block-container {
        padding: 3rem 1.5rem !important;
        max-width: 850px !important;
    }
    
    /* Título Futurista Cromado Neón */
    h1 {
        background: linear-gradient(90deg, #00F0FF, #7000FF, #FF003C);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900 !important;
        font-size: 3.8rem !important;
        text-align: center;
        letter-spacing: 2px;
        margin-bottom: 0px;
        animation: shine 5s linear infinite;
        filter: drop-shadow(0px 0px 15px rgba(0, 240, 255, 0.4));
    }
    
    @keyframes shine {
        to { background-position: 200% center; }
    }
    
    .subtitle {
        text-align: center;
        color: #00F0FF;
        font-weight: 700;
        font-size: 1.1rem;
        letter-spacing: 6px;
        text-transform: uppercase;
        margin-bottom: 3.5rem;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.6);
    }
    
    /* GLOBOS DE CHAT - CRISTAL OSCURO ILUMINADO */
    .stChatMessage {
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.8rem;
        
        /* Dark Glassmorphism */
        background: rgba(10, 10, 25, 0.45) !important;
        backdrop-filter: blur(25px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(25px) saturate(180%) !important;
        
        /* Reflejos Sci-Fi */
        border-top: 1px solid rgba(0, 240, 255, 0.4) !important;
        border-bottom: 1px solid rgba(255, 0, 60, 0.2) !important;
        
        box-shadow: 
            0 15px 35px rgba(0, 0, 0, 0.5),
            inset 0 0 20px rgba(112, 0, 255, 0.1) !important;
        
        animation: dataDrop 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
    }
    
    /* Bot = Bordes Neón Azul/Morado */
    [data-testid="stChatMessage"]:nth-child(odd) {
        border-left: 2px solid #00F0FF !important;
        border-right: 1px solid rgba(255,255,255,0.05) !important;
    }
    
    /* Usuario = Bordes Neón Magenta */
    [data-testid="stChatMessage"]:nth-child(even) {
        background: rgba(20, 10, 30, 0.45) !important;
        border-right: 2px solid #FF003C !important;
        border-left: 1px solid rgba(255,255,255,0.05) !important;
        text-align: right;
    }
    
    @keyframes dataDrop {
        from { opacity: 0; transform: translateY(-20px) scale(0.97); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }
    
    /* INPUT DE CHAT - CONSOLA CYBERPUNK */
    [data-testid="stChatInput"] {
        border-radius: 12px !important;
        background: rgba(5, 5, 15, 0.6) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        
        border: 1px solid rgba(0, 240, 255, 0.3) !important;
        border-bottom: 3px solid #7000FF !important;
        
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7) !important;
        padding: 0.6rem 1.2rem !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stChatInput"]:focus-within {
        background: rgba(10, 10, 25, 0.8) !important;
        border-color: #00F0FF !important;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.2), inset 0 0 10px rgba(0, 240, 255, 0.1) !important;
    }
    
    /* Ajuste de Texto para lectura en Sci-Fi */
    .stMarkdown p { 
        font-size: 1.05rem; 
        color: #E0E0FF; 
        line-height: 1.7;
        font-weight: 300;
    }
    
    .stMarkdown strong {
        color: #00F0FF;
        font-weight: 700;
        text-shadow: 0 0 8px rgba(0, 240, 255, 0.3);
    }
    
    /* Sidebar Terminal de Navegación */
    [data-testid="stSidebar"] {
        background: rgba(5, 5, 15, 0.5) !important;
        backdrop-filter: blur(30px) !important;
        -webkit-backdrop-filter: blur(30px) !important;
        border-right: 1px solid rgba(0, 240, 255, 0.2) !important;
    }
    
</style>
""", unsafe_allow_html=True)

# --- Encabezado ---
st.markdown("<h1>BIMBAM BUY</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>S I S T E M A &nbsp; N Ú C L E O</p>", unsafe_allow_html=True)

# --- Inicialización del Sistema ---
@st.cache_resource(show_spinner="Activando red neuronal...")
def inicializar_sistema():
    if not os.path.exists("chroma_db"):
        st.info("Sincronizando clúster de datos...")
        ejecutar_indexacion()
    return AgenteBimBam()

agente = inicializar_sistema()

# --- Gestión del Historial de Chat ---
if "mensajes" not in st.session_state:
    st.session_state.mensajes = [
        {
            "role": "assistant", 
            "content": "Conexión establecida. 👋 Bienvenido al núcleo de información de BimBam Buy.\n\nPoseo los datos de **Envíos, Garantías, Reembolsos, Pagos y Programa de Afiliados**.\n\n¿Qué bloque de datos deseas consultar?",
            "avatar": "🤖"
        }
    ]

# Mostrar los mensajes
for mensaje in st.session_state.mensajes:
    avatar = mensaje.get("avatar", "⚡" if mensaje["role"] == "user" else "🤖")
    with st.chat_message(mensaje["role"], avatar=avatar):
        st.markdown(mensaje["content"])

# --- Entrada de Usuario ---
pregunta_usuario = st.chat_input("Inicializar comando...")

if pregunta_usuario:
    st.session_state.mensajes.append({"role": "user", "content": pregunta_usuario, "avatar": "⚡"})
    with st.chat_message("user", avatar="⚡"):
        st.markdown(pregunta_usuario)
    
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Procesando matriz de datos..."):
            resultado = agente.preguntar(pregunta_usuario)
            respuesta_texto = resultado["respuesta"]
            st.markdown(respuesta_texto)
            
    st.session_state.mensajes.append({
        "role": "assistant", 
        "content": respuesta_texto,
        "avatar": "🤖"
    })

# --- Barra Lateral ---
with st.sidebar:
    st.markdown("### 🎛️ Terminal Principal")
    st.markdown("""
    Protocolo **RAG** en línea.
    """)
    st.divider()
    st.markdown("#### 💾 Nodos Activos:")
    st.caption("⚡ Tiempos y Costos de Envío")
    st.caption("⚡ Manual de Garantía")
    st.caption("⚡ Reembolsos y Devoluciones")
    st.caption("⚡ Métodos de Pago")
    st.caption("⚡ Programa de Afiliados")
    st.divider()
    
    if st.button("🔌 Purgar Memoria", type="primary", use_container_width=True):
        st.session_state.mensajes = [
            {"role": "assistant", "content": "Memoria purgada. Esperando nuevos comandos. 🤖", "avatar": "🤖"}
        ]
        agente.reiniciar_conversacion()
        st.rerun()
