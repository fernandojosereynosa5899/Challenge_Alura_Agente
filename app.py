"""
Interfaz web del Agente BimBam Buy.
Estilo: Cálido, hogareño y amigable.
"""
import streamlit as st
from src.agente import AgenteBimBam
from src.indexador import ejecutar_indexacion
import os

st.set_page_config(
    page_title="BimBam Buy | Ayuda",
    page_icon="🛒",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- CSS Cálido y Hogareño ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif !important;
    }
    
    .stApp { 
        background-color: #FFF8F0;
    }
    
    .main .block-container {
        padding: 2rem 1.5rem !important;
        max-width: 800px !important;
    }
    
    /* Título sencillo y cálido */
    h1 {
        color: #E07A5F !important;
        font-weight: 800 !important;
        font-size: 2.5rem !important;
        text-align: center;
        margin-bottom: 0;
    }
    
    .subtitle {
        text-align: center;
        color: #81B29A;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    /* Cajas de chat suaves y redondeadas */
    .stChatMessage {
        border-radius: 16px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        background: #FFFFFF !important;
        border: 1px solid #F2E9DE;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    
    /* Texto legible y cálido */
    .stMarkdown p { 
        font-size: 1rem; 
        color: #3D405B; 
        line-height: 1.6; 
    }
    
    /* Input redondeado y amigable */
    [data-testid="stChatInput"] {
        border-radius: 24px !important;
        border: 2px solid #F2E9DE !important;
        background: #FFFFFF !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04) !important;
    }
    
    [data-testid="stChatInput"]:focus-within {
        border-color: #E07A5F !important;
        box-shadow: 0 4px 12px rgba(224, 122, 95, 0.15) !important;
    }
    
</style>
""", unsafe_allow_html=True)

# --- Encabezado ---
st.markdown("<h1>🛒 BimBam Buy</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Tu asistente de confianza</p>", unsafe_allow_html=True)

# --- Inicialización ---
@st.cache_resource(show_spinner="Preparando todo para ti...")
def inicializar_sistema():
    if not os.path.exists("chroma_db"):
        ejecutar_indexacion()
    return AgenteBimBam()

agente = inicializar_sistema()

# --- Historial de Chat ---
if "mensajes" not in st.session_state:
    st.session_state.mensajes = [
        {
            "role": "assistant",
            "content": "¡Hola! 😊 Soy tu asistente de BimBam Buy. Puedo ayudarte con dudas sobre **envíos, garantías, reembolsos, pagos y afiliados**.\n\n¿Qué necesitas saber?",
        }
    ]

for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])

# --- Entrada de Usuario ---
pregunta_usuario = st.chat_input("Escribe tu pregunta aquí...")

if pregunta_usuario:
    st.session_state.mensajes.append({"role": "user", "content": pregunta_usuario})
    with st.chat_message("user"):
        st.markdown(pregunta_usuario)

    with st.chat_message("assistant"):
        with st.spinner("Buscando la respuesta..."):
            resultado = agente.preguntar(pregunta_usuario)
            respuesta_texto = resultado["respuesta"]
            st.markdown(respuesta_texto)

    st.session_state.mensajes.append({"role": "assistant", "content": respuesta_texto})

# --- Sidebar ---
with st.sidebar:
    st.markdown("### 📖 Sobre este asistente")
    st.markdown("""
    Este chat responde tus preguntas usando los documentos oficiales de BimBam Buy.
    """)
    st.divider()
    st.markdown("**Temas disponibles:**")
    st.markdown("""
    - 📦 Envíos
    - 🛡️ Garantías
    - 💸 Devoluciones
    - 💳 Pagos
    - 🤝 Afiliados
    """)
    st.divider()
    if st.button("🔄 Nueva conversación", use_container_width=True):
        st.session_state.mensajes = [
            {"role": "assistant", "content": "¡Listo! Conversación reiniciada. ¿En qué te ayudo? 😊"}
        ]
        agente.reiniciar_conversacion()
        st.rerun()
