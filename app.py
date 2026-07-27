"""
Interfaz web del Agente BimBam Buy.
Estilo: Cálido y hogareño con animaciones sutiles.
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

# --- CSS Cálido con Animaciones Sutiles ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif !important;
    }
    
    /* Fondo con gradiente muy suave que respira lentamente */
    .stApp { 
        background: linear-gradient(160deg, #FFF8F0 0%, #FFF1E6 30%, #F0F7F4 70%, #FFF8F0 100%);
        background-size: 200% 200%;
        animation: breathe 20s ease-in-out infinite;
    }
    
    @keyframes breathe {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .main .block-container {
        padding: 2rem 1.5rem !important;
        max-width: 800px !important;
    }
    
    /* Título con aparición suave */
    h1 {
        color: #E07A5F !important;
        font-weight: 800 !important;
        font-size: 2.5rem !important;
        text-align: center;
        margin-bottom: 0;
        animation: fadeDown 0.8s ease-out;
    }
    
    @keyframes fadeDown {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .subtitle {
        text-align: center;
        color: #81B29A;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        animation: fadeDown 1s ease-out;
    }
    
    /* Cajas de chat con entrada suave */
    .stChatMessage {
        border-radius: 16px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        background: #FFFFFF !important;
        border: 1px solid #F2E9DE;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        animation: slideIn 0.4s ease-out;
        transition: box-shadow 0.3s ease, transform 0.3s ease;
    }
    
    .stChatMessage:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.07);
        transform: translateY(-1px);
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Texto legible y cálido */
    .stMarkdown p { 
        font-size: 1rem; 
        color: #3D405B; 
        line-height: 1.6; 
    }
    
    /* Input con transición suave al enfocar */
    [data-testid="stChatInput"] {
        border-radius: 24px !important;
        border: 2px solid #F2E9DE !important;
        background: #FFFFFF !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04) !important;
        transition: all 0.4s ease !important;
    }
    
    [data-testid="stChatInput"]:focus-within {
        border-color: #E07A5F !important;
        box-shadow: 0 4px 18px rgba(224, 122, 95, 0.12) !important;
        transform: translateY(-1px);
    }
    
    /* Botón sidebar con hover elegante */
    .stButton > button {
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
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
