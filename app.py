"""
Interfaz web del Agente BimBam Buy.
Estilo: Cálido y hogareño con animaciones sutiles e iconos SVG.
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
    
    /* Encabezado personalizado */
    .header-container {
        text-align: center;
        margin-bottom: 2rem;
        animation: fadeDown 0.8s ease-out;
    }
    
    .header-container svg {
        margin-bottom: 8px;
    }
    
    .header-container h1 {
        color: #E07A5F !important;
        font-weight: 800 !important;
        font-size: 2.5rem !important;
        margin: 0 !important;
    }
    
    .header-container p {
        color: #81B29A;
        font-weight: 600;
        font-size: 1.1rem;
        margin-top: 4px;
    }
    
    @keyframes fadeDown {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
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
    
    /* Texto */
    .stMarkdown p { 
        font-size: 1rem; 
        color: #3D405B; 
        line-height: 1.6; 
    }
    
    /* Input */
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
    
    /* Sidebar items con iconos */
    .sidebar-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 12px;
        margin-bottom: 6px;
        border-radius: 10px;
        background: rgba(255,255,255,0.6);
        transition: background 0.3s ease, transform 0.2s ease;
    }
    
    .sidebar-item:hover {
        background: rgba(224, 122, 95, 0.08);
        transform: translateX(4px);
    }
    
    .sidebar-item svg {
        flex-shrink: 0;
    }
    
    .sidebar-item span {
        font-size: 0.95rem;
        color: #3D405B;
        font-weight: 600;
    }
    
    .stButton > button {
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-1px) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Encabezado con SVG ---
st.markdown("""
<div class="header-container">
    <svg width="56" height="56" viewBox="0 0 24 24" fill="none">
        <circle cx="12" cy="12" r="12" fill="#E07A5F" opacity="0.12"/>
        <path d="M7 18C5.9 18 5 17.1 5 16V8C5 6.9 5.9 6 7 6H8L9.5 4H14.5L16 6H17C18.1 6 19 6.9 19 8V16C19 17.1 18.1 18 17 18H7Z" fill="none" stroke="#E07A5F" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M9 11L11 13L15 9" stroke="#81B29A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    <h1>BimBam Buy</h1>
    <p>Tu asistente de confianza</p>
</div>
""", unsafe_allow_html=True)

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

# --- Sidebar con iconos SVG ---
with st.sidebar:
    st.markdown("### Acerca de")
    st.markdown("""
    Este chat responde tus preguntas usando los documentos oficiales de BimBam Buy.
    """)
    st.divider()
    st.markdown("**Temas disponibles:**")

    # Envíos
    st.markdown("""
    <div class="sidebar-item">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
            <rect x="1" y="6" width="15" height="13" rx="2" stroke="#E07A5F" stroke-width="1.5"/>
            <path d="M16 10H20L23 13V17H16V10Z" stroke="#E07A5F" stroke-width="1.5" stroke-linejoin="round"/>
            <circle cx="6.5" cy="19.5" r="1.5" fill="#81B29A" stroke="#81B29A"/>
            <circle cx="19.5" cy="19.5" r="1.5" fill="#81B29A" stroke="#81B29A"/>
        </svg>
        <span>Envíos y logística</span>
    </div>
    """, unsafe_allow_html=True)

    # Garantías
    st.markdown("""
    <div class="sidebar-item">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
            <path d="M12 2L3 7V12C3 17.5 6.8 22.7 12 24C17.2 22.7 21 17.5 21 12V7L12 2Z" stroke="#E07A5F" stroke-width="1.5" stroke-linejoin="round"/>
            <path d="M9 12L11 14L15 10" stroke="#81B29A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>Garantías</span>
    </div>
    """, unsafe_allow_html=True)

    # Devoluciones
    st.markdown("""
    <div class="sidebar-item">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
            <path d="M3 10H13C16.9 10 20 13.1 20 17V18" stroke="#E07A5F" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M7 6L3 10L7 14" stroke="#E07A5F" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            <line x1="20" y1="18" x2="20" y2="22" stroke="#81B29A" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        <span>Devoluciones</span>
    </div>
    """, unsafe_allow_html=True)

    # Pagos
    st.markdown("""
    <div class="sidebar-item">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
            <rect x="2" y="5" width="20" height="14" rx="2" stroke="#E07A5F" stroke-width="1.5"/>
            <line x1="2" y1="10" x2="22" y2="10" stroke="#E07A5F" stroke-width="1.5"/>
            <rect x="5" y="14" width="5" height="2" rx="1" fill="#81B29A"/>
        </svg>
        <span>Métodos de pago</span>
    </div>
    """, unsafe_allow_html=True)

    # Afiliados
    st.markdown("""
    <div class="sidebar-item">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
            <circle cx="9" cy="7" r="3" stroke="#E07A5F" stroke-width="1.5"/>
            <path d="M3 21V18C3 16.3 4.3 15 6 15H12C13.7 15 15 16.3 15 18V21" stroke="#E07A5F" stroke-width="1.5" stroke-linecap="round"/>
            <path d="M17 11L19 13L23 9" stroke="#81B29A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span>Programa de Afiliados</span>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    if st.button("🔄 Nueva conversación", use_container_width=True):
        st.session_state.mensajes = [
            {"role": "assistant", "content": "¡Listo! Conversación reiniciada. ¿En qué te ayudo? 😊"}
        ]
        agente.reiniciar_conversacion()
        st.rerun()
