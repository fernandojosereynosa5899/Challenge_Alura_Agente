"""
Interfaz web del Agente BimBam Buy construida con Streamlit.
Corresponde a la tarjeta 6 (Interfaz) del tablero Trello.

Proporciona un chat interactivo donde los colaboradores pueden hacer preguntas
y visualizar las fuentes de donde se extrajo la información.
"""
import streamlit as st
from src.agente import AgenteBimBam
from src.indexador import ejecutar_indexacion
import os

# --- Configuración de la página ---
st.set_page_config(
    page_title="BimBam Buy | IA",
    page_icon="🛍️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- CSS Premium y Animaciones ---
st.markdown("""
<style>
    /* Tipografía y espaciado general */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Contenedor principal */
    .stApp { 
        max-width: 900px; 
        margin: 0 auto; 
    }
    
    /* Títulos con gradiente */
    h1 {
        background: linear-gradient(90deg, #2A62C9, #10B981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        letter-spacing: -1px;
    }
    
    /* Tarjetas de fuentes (Source Tags) con efecto Hover */
    .fuente-tag {
        background: linear-gradient(135deg, #EFF6FF, #DBEAFE);
        color: #1E3A8A;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.85em;
        font-weight: 600;
        margin: 4px;
        display: inline-block;
        border: 1px solid #BFDBFE;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .fuente-tag:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        background: linear-gradient(135deg, #DBEAFE, #BFDBFE);
    }
    
    /* Globos de chat con Glassmorphism suave */
    .stChatMessage {
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02);
        animation: fadeIn 0.5s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Input de chat mejorado */
    [data-testid="stChatInput"] {
        border-radius: 24px !important;
        border: 2px solid #E2E8F0 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stChatInput"]:focus-within {
        border-color: #2A62C9 !important;
        box-shadow: 0 4px 15px rgba(42, 98, 201, 0.15) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- Encabezado ---
st.title("🛍️ BimBam Buy")
st.markdown("### ✨ Asistente Inteligente Corporativo")
st.markdown("---")

# --- Inicialización del Agente ---
@st.cache_resource(show_spinner="Configurando tu asistente virtual...")
def inicializar_agente():
    if not os.path.exists("chroma_db"):
        st.info("Primera ejecución detectada. Indexando documentos oficiales...")
        ejecutar_indexacion()
    return AgenteBimBam()

agente = inicializar_agente()

# --- Gestión del Historial de Chat ---
if "mensajes" not in st.session_state:
    st.session_state.mensajes = [
        {"role": "assistant", "content": "¡Hola! 👋 Soy la Inteligencia Artificial de BimBam Buy. Estoy entrenado con nuestras políticas de Envíos, Garantías, Reembolsos, Pagos y Afiliados. **¿En qué te puedo ayudar hoy?**"}
    ]

# Mostrar los mensajes anteriores
for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])
        if "fuentes" in mensaje and mensaje["fuentes"]:
            st.markdown("<br>**📚 Fuentes oficiales consultadas:**", unsafe_allow_html=True)
            for fuente in mensaje["fuentes"]:
                st.markdown(f"<span class='fuente-tag'>📄 {fuente}</span>", unsafe_allow_html=True)

# --- Entrada de Usuario ---
pregunta_usuario = st.chat_input("Ej: ¿Cuál es el proceso para tramitar una garantía?")

if pregunta_usuario:
    # 1. Mostrar la pregunta del usuario
    with st.chat_message("user"):
        st.markdown(pregunta_usuario)
    
    st.session_state.mensajes.append({"role": "user", "content": pregunta_usuario})
    
    # 2. Generar y mostrar la respuesta
    with st.chat_message("assistant"):
        with st.spinner("Analizando manuales corporativos..."):
            resultado = agente.preguntar(pregunta_usuario)
            
            respuesta_texto = resultado["respuesta"]
            fuentes = resultado["fuentes"]
            
            st.markdown(respuesta_texto)
            
            if fuentes:
                st.markdown("<br>**📚 Fuentes oficiales consultadas:**", unsafe_allow_html=True)
                for fuente in fuentes:
                    st.markdown(f"<span class='fuente-tag'>📄 {fuente}</span>", unsafe_allow_html=True)
            
    # 3. Guardar en historial
    st.session_state.mensajes.append({
        "role": "assistant", 
        "content": respuesta_texto,
        "fuentes": fuentes
    })

# --- Barra Lateral (Sidebar) ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/online-store.png", width=60)
    st.header("Centro de Conocimiento")
    st.markdown("""
    Este asistente utiliza tecnología **RAG de vanguardia** para responder 
    preguntas basándose **únicamente** en los documentos internos oficiales de la empresa.
    """)
    
    st.divider()
    
    st.subheader("📑 Políticas Indexadas:")
    st.markdown("""
    - 📦 Tiempos y Costos de Envío
    - 🛡️ Manual de Garantía
    - 💸 Reembolsos y Devoluciones
    - 💳 FAQ de Métodos de Pago
    - 🤝 Programa de Afiliados
    """)
    
    st.divider()
    
    if st.button("✨ Reiniciar Sesión", type="primary", use_container_width=True):
        st.session_state.mensajes = [
            {"role": "assistant", "content": "¡Conversación reiniciada! 👋 ¿En qué más te puedo asistir?"}
        ]
        agente.reiniciar_conversacion()
        st.rerun()
    
    st.caption("🔒 Respuestas protegidas y basadas 100% en documentación interna. No incluye información de internet.")
