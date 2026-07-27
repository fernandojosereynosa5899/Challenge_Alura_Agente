"""
Interfaz web del Agente BimBam Buy construida con Streamlit.
Corresponde a la tarjeta 6 (Interfaz) del tablero Trello.
"""
import streamlit as st
from src.agente import AgenteBimBam
from src.indexador import ejecutar_indexacion
import os

# --- Configuración de la página ---
st.set_page_config(
    page_title="BimBam Buy | Asistente IA",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="expanded"
)

# --- CSS Ultra Premium Final ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    /* Fondo limpio y muy moderno */
    .stApp { 
        background-color: #FAFAFB;
        background-image: radial-gradient(at 8% 13%, hsla(253,88%,79%,0.15) 0px, transparent 50%),
                          radial-gradient(at 89% 82%, hsla(334,91%,79%,0.12) 0px, transparent 50%);
        background-attachment: fixed;
    }
    
    /* Título Impresionante */
    .titulo-principal {
        background: linear-gradient(135deg, #4F46E5 0%, #D946EF 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        font-size: 3.5rem !important;
        text-align: center;
        margin-bottom: 0px;
        line-height: 1.2;
    }
    
    .subtitulo {
        text-align: center;
        color: #64748B;
        font-weight: 500;
        font-size: 1.2rem;
        margin-bottom: 2.5rem;
    }
    
    /* Contenedor central ajustado */
    .main .block-container {
        padding: 3rem 1.5rem !important;
        max-width: 850px !important;
    }
    
    /* Estilos de las cajas de Chat */
    .stChatMessage {
        border-radius: 16px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
        border: 1px solid rgba(255, 255, 255, 0.8);
        animation: scaleIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
        background: white;
    }
    
    /* Mensajes del Bot */
    [data-testid="stChatMessage"]:nth-child(odd) {
        background: linear-gradient(145deg, #ffffff, #f8faff);
        border-left: 4px solid #8B5CF6;
    }
    
    /* Mensajes del Usuario */
    [data-testid="stChatMessage"]:nth-child(even) {
        background: linear-gradient(145deg, #F3E8FF, #FaF5FF);
        border-right: 4px solid #D946EF;
    }
    
    @keyframes scaleIn {
        from { opacity: 0; transform: scale(0.97) translateY(10px); }
        to { opacity: 1; transform: scale(1) translateY(0); }
    }
    
    /* Etiquetas de Fuentes Premium */
    .fuente-tag {
        background: linear-gradient(90deg, #3B82F6, #8B5CF6);
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin: 4px 4px 4px 0;
        display: inline-flex;
        align-items: center;
        box-shadow: 0 2px 8px rgba(139, 92, 246, 0.3);
        transition: transform 0.2s;
    }
    .fuente-tag:hover {
        transform: translateY(-2px);
    }
    
    /* Input de Chat Flotante */
    [data-testid="stChatInput"] {
        border-radius: 20px !important;
        border: 1px solid #E2E8F0 !important;
        background: white !important;
        box-shadow: 0 10px 25px rgba(139, 92, 246, 0.08) !important;
        padding: 0.3rem 0.5rem !important;
    }
    
    [data-testid="stChatInput"]:focus-within {
        border-color: #8B5CF6 !important;
        box-shadow: 0 10px 30px rgba(139, 92, 246, 0.15) !important;
    }
    
    /* Ajustes visuales para Markdown */
    .stMarkdown p { font-size: 1.05rem; color: #334155; line-height: 1.6; }
    .stMarkdown h3 { color: #1E293B; }
    
</style>
""", unsafe_allow_html=True)

# --- Encabezado ---
st.markdown("<h1 class='titulo-principal'>BimBam Buy AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitulo'>Tu Copiloto Corporativo Inteligente ✨</p>", unsafe_allow_html=True)

# --- Inicialización del Agente ---
@st.cache_resource(show_spinner="Preparando el cerebro del asistente...")
def inicializar_agente():
    if not os.path.exists("chroma_db"):
        st.info("Sincronizando conocimientos. Esto tomará unos segundos...")
        ejecutar_indexacion()
    return AgenteBimBam()

agente = inicializar_agente()

# --- Gestión del Historial de Chat ---
if "mensajes" not in st.session_state:
    st.session_state.mensajes = [
        {
            "role": "assistant", 
            "content": "**¡Hola! 👋** Bienvenido a la base de conocimiento de BimBam Buy.\n\nEstoy entrenado para responder cualquier duda sobre nuestras **Políticas de Envíos, Garantías, Reembolsos, Pagos y el Programa de Afiliados**.\n\n*¿En qué te puedo ayudar hoy?*",
            "avatar": "✨"
        }
    ]

# Mostrar los mensajes anteriores
for mensaje in st.session_state.mensajes:
    avatar = mensaje.get("avatar", "🧑‍💻" if mensaje["role"] == "user" else "✨")
    with st.chat_message(mensaje["role"], avatar=avatar):
        st.markdown(mensaje["content"])
        if "fuentes" in mensaje and mensaje["fuentes"]:
            st.markdown("<br><span style='color: #94A3B8; font-size: 0.75rem; font-weight: 700; letter-spacing: 1px;'>FUENTES OFICIALES:</span><br>", unsafe_allow_html=True)
            for fuente in mensaje["fuentes"]:
                nombre_limpio = fuente.replace('_', ' ').replace('.pdf', '')
                st.markdown(f"<span class='fuente-tag'>📄 {nombre_limpio}</span>", unsafe_allow_html=True)

# --- Entrada de Usuario ---
pregunta_usuario = st.chat_input("Escribe tu consulta aquí...")

if pregunta_usuario:
    # 1. Mostrar la pregunta del usuario
    st.session_state.mensajes.append({"role": "user", "content": pregunta_usuario, "avatar": "🧑‍💻"})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(pregunta_usuario)
    
    # 2. Generar y mostrar la respuesta
    with st.chat_message("assistant", avatar="✨"):
        with st.spinner("Consultando los manuales corporativos..."):
            resultado = agente.preguntar(pregunta_usuario)
            
            respuesta_texto = resultado["respuesta"]
            fuentes = resultado["fuentes"]
            
            st.markdown(respuesta_texto)
            
            if fuentes:
                st.markdown("<br><span style='color: #94A3B8; font-size: 0.75rem; font-weight: 700; letter-spacing: 1px;'>FUENTES OFICIALES:</span><br>", unsafe_allow_html=True)
                for fuente in fuentes:
                    nombre_limpio = fuente.replace('_', ' ').replace('.pdf', '')
                    st.markdown(f"<span class='fuente-tag'>📄 {nombre_limpio}</span>", unsafe_allow_html=True)
            
    # 3. Guardar en historial
    st.session_state.mensajes.append({
        "role": "assistant", 
        "content": respuesta_texto,
        "fuentes": fuentes,
        "avatar": "✨"
    })

# --- Barra Lateral (Sidebar) ---
with st.sidebar:
    st.markdown("### ⚙️ Panel de Control")
    st.markdown("""
    Este asistente utiliza **Inteligencia Artificial (RAG)**.  
    Toda respuesta está respaldada estrictamente por la documentación oficial.
    """)
    
    st.divider()
    
    st.markdown("#### 📖 Módulos Indexados:")
    st.markdown("""
    - 📦 Tiempos y Costos de Envío
    - 🛡️ Manual de Garantía
    - 💸 Reembolsos y Devoluciones
    - 💳 FAQ de Métodos de Pago
    - 🤝 Programa de Afiliados
    """)
    
    st.divider()
    
    if st.button("🔄 Reiniciar Sesión", type="primary", use_container_width=True):
        st.session_state.mensajes = [
            {"role": "assistant", "content": "¡Memoria borrada! Comenzamos de nuevo. ✨", "avatar": "✨"}
        ]
        agente.reiniciar_conversacion()
        st.rerun()
