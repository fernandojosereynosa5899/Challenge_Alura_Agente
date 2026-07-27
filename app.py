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
    page_title="BimBam Buy | IA",
    page_icon="✨",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- CSS Ultra Premium, Responsivo y Vibrante ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* Contenedor principal con efecto de desenfoque de fondo */
    .stApp { 
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
    }
    
    /* Título Impresionante con Gradiente Dinámico */
    h1 {
        background: linear-gradient(-45deg, #8B5CF6, #EC4899, #F43F5E, #8B5CF6);
        background-size: 300% 300%;
        animation: gradientBG 5s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        font-size: 3rem !important;
        text-align: center;
        margin-bottom: -10px;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Contenedor responsivo */
    .main .block-container {
        padding: 2rem 1rem !important;
        max-width: 900px !important;
    }
    
    /* Globos de Chat Estilo iMessage/Glassmorphism */
    .stChatMessage {
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.05);
        animation: slideUp 0.4s ease-out forwards;
        background: rgba(255, 255, 255, 0.85);
    }
    
    /* Diferenciar el globo del usuario del bot */
    [data-testid="stChatMessage"]:nth-child(even) {
        background: linear-gradient(135deg, #F3E8FF, #FCE7F3);
        border: 1px solid #FBCFE8;
    }
    
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px) scale(0.98); }
        to { opacity: 1; transform: translateY(0) scale(1); }
    }
    
    /* Etiquetas de Fuentes (Píldoras de colores vibrantes) */
    .fuente-tag {
        background: linear-gradient(90deg, #6366F1, #8B5CF6);
        color: white;
        padding: 6px 14px;
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 500;
        margin: 4px;
        display: inline-flex;
        align-items: center;
        box-shadow: 0 4px 10px rgba(139, 92, 246, 0.3);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .fuente-tag:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 15px rgba(139, 92, 246, 0.5);
    }
    
    /* Input de Chat Elevado y Responsivo */
    [data-testid="stChatInput"] {
        border-radius: 30px !important;
        border: 2px solid #E2E8F0 !important;
        background: rgba(255, 255, 255, 0.9) !important;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05) !important;
        padding: 0.2rem 1rem !important;
    }
    
    [data-testid="stChatInput"]:focus-within {
        border-color: #8B5CF6 !important;
        box-shadow: 0 10px 30px rgba(139, 92, 246, 0.2) !important;
    }

    /* Media Queries para Responsividad (Celulares) */
    @media (max-width: 768px) {
        h1 { font-size: 2.2rem !important; }
        .stChatMessage { padding: 1rem; }
        .fuente-tag { font-size: 0.75rem; padding: 5px 10px; }
    }
</style>
""", unsafe_allow_html=True)

# --- Encabezado ---
st.markdown("<h1>✨ BimBam Buy AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748B; font-size: 1.1rem; margin-bottom: 2rem;'>Tu Asistente Corporativo Inteligente</p>", unsafe_allow_html=True)

# --- Inicialización del Agente ---
@st.cache_resource(show_spinner="Despertando a la IA...")
def inicializar_agente():
    if not os.path.exists("chroma_db"):
        st.info("Sincronizando conocimientos. Esto tomará unos segundos...")
        ejecutar_indexacion()
    return AgenteBimBam()

agente = inicializar_agente()

# --- Gestión del Historial de Chat ---
if "mensajes" not in st.session_state:
    st.session_state.mensajes = [
        {"role": "assistant", "content": "¡Hola! 👋 Soy tu copiloto en BimBam Buy. Conozco a la perfección todas nuestras **Políticas de Envíos, Garantías, Reembolsos, Pagos y Afiliados**.\n\n¿Qué duda tienes hoy?"}
    ]

# Mostrar los mensajes anteriores
for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])
        if "fuentes" in mensaje and mensaje["fuentes"]:
            st.markdown("<br><span style='color: #64748B; font-size: 0.85rem;'>📚 F U E N T E S :</span><br>", unsafe_allow_html=True)
            for fuente in mensaje["fuentes"]:
                # Formatear el nombre del PDF para que se vea más limpio
                nombre_limpio = fuente.replace('_', ' ').replace('.pdf', '')
                st.markdown(f"<span class='fuente-tag'>📄 {nombre_limpio}</span>", unsafe_allow_html=True)

# --- Entrada de Usuario ---
pregunta_usuario = st.chat_input("Escribe tu consulta aquí...")

if pregunta_usuario:
    # 1. Mostrar la pregunta del usuario
    with st.chat_message("user"):
        st.markdown(pregunta_usuario)
    
    st.session_state.mensajes.append({"role": "user", "content": pregunta_usuario})
    
    # 2. Generar y mostrar la respuesta
    with st.chat_message("assistant"):
        with st.spinner("Analizando la matriz de documentos..."):
            resultado = agente.preguntar(pregunta_usuario)
            
            respuesta_texto = resultado["respuesta"]
            fuentes = resultado["fuentes"]
            
            st.markdown(respuesta_texto)
            
            if fuentes:
                st.markdown("<br><span style='color: #64748B; font-size: 0.85rem;'>📚 F U E N T E S :</span><br>", unsafe_allow_html=True)
                for fuente in fuentes:
                    nombre_limpio = fuente.replace('_', ' ').replace('.pdf', '')
                    st.markdown(f"<span class='fuente-tag'>📄 {nombre_limpio}</span>", unsafe_allow_html=True)
            
    # 3. Guardar en historial
    st.session_state.mensajes.append({
        "role": "assistant", 
        "content": respuesta_texto,
        "fuentes": fuentes
    })

# --- Barra Lateral (Sidebar) Responsiva ---
with st.sidebar:
    st.markdown("### ⚙️ Panel de Control")
    st.markdown("""
    Este asistente utiliza **Inteligencia Artificial (RAG)**.  
    Toda respuesta está respaldada estrictamente por la documentación de la empresa.
    """)
    
    st.divider()
    
    st.markdown("#### 📖 Archivos Base:")
    st.caption("✔️ Envíos y Logística")
    st.caption("✔️ Cobertura de Garantías")
    st.caption("✔️ Devoluciones")
    st.caption("✔️ Medios de Pago")
    st.caption("✔️ Afiliados")
    
    st.divider()
    
    if st.button("🗑️ Borrar Historial", type="primary", use_container_width=True):
        st.session_state.mensajes = [
            {"role": "assistant", "content": "¡Memoria borrada! Comenzamos de nuevo. ✨"}
        ]
        agente.reiniciar_conversacion()
        st.rerun()
