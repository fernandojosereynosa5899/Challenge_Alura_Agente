"""
Interfaz web del Agente BimBam Buy.
Estilo: Liquid Crystal (Vibrante, Glassmorphism avanzado)
"""
import streamlit as st
from src.agente import AgenteBimBam
from src.indexador import ejecutar_indexacion
import os

st.set_page_config(
    page_title="BimBam Buy | IA",
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- CSS Estilo LIQUID CRYSTAL ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Fondo con Mesh Gradient dinámico simulando líquido */
    .stApp { 
        background-color: #f6f8fd;
        background-image: 
            radial-gradient(at 0% 0%, rgba(139, 92, 246, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(56, 189, 248, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(236, 72, 153, 0.15) 0px, transparent 50%),
            radial-gradient(at 0% 100%, rgba(16, 185, 129, 0.15) 0px, transparent 50%);
        background-attachment: fixed;
    }
    
    /* Contenedor central más ancho y limpio */
    .main .block-container {
        padding: 3rem 1.5rem !important;
        max-width: 850px !important;
    }
    
    /* Título con textura de cristal líquido */
    h1 {
        background: linear-gradient(to right, #6366f1, #06b6d4, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        font-size: 3.8rem !important;
        text-align: center;
        letter-spacing: -1.5px;
        margin-bottom: 0px;
        filter: drop-shadow(0px 4px 10px rgba(99, 102, 241, 0.2));
    }
    
    .subtitle {
        text-align: center;
        color: #475569;
        font-weight: 500;
        font-size: 1.3rem;
        margin-bottom: 3rem;
    }
    
    /* Efecto Liquid Crystal en Cajas de Chat */
    .stChatMessage {
        border-radius: 24px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        
        /* Glassmorphism */
        background: rgba(255, 255, 255, 0.45);
        backdrop-filter: blur(16px) saturate(180%);
        -webkit-backdrop-filter: blur(16px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.8);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.05);
        
        animation: floatIn 0.5s cubic-bezier(0.23, 1, 0.32, 1) forwards;
    }
    
    /* Bot = Tono Azul/Púrpura Cristalino */
    [data-testid="stChatMessage"]:nth-child(odd) {
        border-left: 2px solid rgba(139, 92, 246, 0.4);
        border-top: 1px solid rgba(255, 255, 255, 0.9);
    }
    
    /* Usuario = Tono Cyan/Verde Cristalino */
    [data-testid="stChatMessage"]:nth-child(even) {
        background: rgba(255, 255, 255, 0.6);
        border-right: 2px solid rgba(56, 189, 248, 0.4);
        text-align: right;
    }
    
    /* Animación de entrada suave */
    @keyframes floatIn {
        from { opacity: 0; transform: translateY(20px) scale(0.98); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }
    
    /* Input de Chat Estilo Píldora de Cristal */
    [data-testid="stChatInput"] {
        border-radius: 30px !important;
        border: 1px solid rgba(255, 255, 255, 0.8) !important;
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.04) !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stChatInput"]:focus-within {
        background: rgba(255, 255, 255, 0.95) !important;
        border-color: rgba(56, 189, 248, 0.5) !important;
        box-shadow: 0 15px 35px rgba(56, 189, 248, 0.15) !important;
        transform: translateY(-2px);
    }
    
    /* Tipografía interior del chat */
    .stMarkdown p { font-size: 1.05rem; color: #1e293b; line-height: 1.6; }
    
</style>
""", unsafe_allow_html=True)

# --- Encabezado ---
st.markdown("<h1>BimBam Buy AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Tu Inteligencia Operativa ✨</p>", unsafe_allow_html=True)

# --- Inicialización del Sistema ---
@st.cache_resource(show_spinner="Cristalizando base de conocimiento...")
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
            "avatar": "🔮"
        }
    ]

# Mostrar los mensajes
for mensaje in st.session_state.mensajes:
    avatar = mensaje.get("avatar", "👤" if mensaje["role"] == "user" else "🔮")
    with st.chat_message(mensaje["role"], avatar=avatar):
        st.markdown(mensaje["content"])

# --- Entrada de Usuario ---
pregunta_usuario = st.chat_input("Escribe tu pregunta aquí...")

if pregunta_usuario:
    # Mostrar la pregunta del usuario
    st.session_state.mensajes.append({"role": "user", "content": pregunta_usuario, "avatar": "👤"})
    with st.chat_message("user", avatar="👤"):
        st.markdown(pregunta_usuario)
    
    # Generar y mostrar la respuesta
    with st.chat_message("assistant", avatar="🔮"):
        with st.spinner("Sintetizando información..."):
            resultado = agente.preguntar(pregunta_usuario)
            respuesta_texto = resultado["respuesta"]
            
            # Solo mostramos la respuesta, ocultando las fuentes.
            st.markdown(respuesta_texto)
            
    # Guardar en historial
    st.session_state.mensajes.append({
        "role": "assistant", 
        "content": respuesta_texto,
        "avatar": "🔮"
    })

# --- Barra Lateral (Sidebar) Efecto Cristal ---
with st.sidebar:
    st.markdown("### 🎛️ Centro de Control")
    st.markdown("""
    Desarrollado con arquitectura **RAG**.
    """)
    
    st.divider()
    
    st.markdown("#### 📚 Documentos Base:")
    st.caption("✨ Tiempos y Costos de Envío")
    st.caption("✨ Manual de Garantía")
    st.caption("✨ Reembolsos y Devoluciones")
    st.caption("✨ Métodos de Pago")
    st.caption("✨ Programa de Afiliados")
    
    st.divider()
    
    if st.button("💫 Reiniciar Sesión", type="primary", use_container_width=True):
        st.session_state.mensajes = [
            {"role": "assistant", "content": "Sesión reiniciada. ¡Comenzamos de nuevo! ✨", "avatar": "🔮"}
        ]
        agente.reiniciar_conversacion()
        st.rerun()
