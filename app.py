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
    page_title="🛒 Asistente BimBam Buy",
    page_icon="🤖",
    layout="centered",
)

# --- CSS Personalizado ---
st.markdown("""
<style>
    /* Estilos para que se vea más limpio */
    .stApp { max-width: 900px; margin: 0 auto; }
    .fuente-tag {
        background-color: #e8f4fd;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.85em;
        margin: 2px;
        display: inline-block;
        border: 1px solid #b3d4fc;
    }
</style>
""", unsafe_allow_html=True)

# --- Encabezado ---
st.title("🛒 BimBam Buy")
st.subheader("🤖 Asistente IA para Colaboradores")
st.markdown("---")

# --- Inicialización del Agente ---
# Usamos st.cache_resource para que el agente se cargue solo una vez
@st.cache_resource(show_spinner="Inicializando base de conocimiento...")
def inicializar_agente():
    # Verificamos si existe la base de datos, si no, la creamos (indexación automática)
    if not os.path.exists("chroma_db"):
        st.info("Primera ejecución detectada. Indexando documentos...")
        ejecutar_indexacion()
    return AgenteBimBam()

# Cargamos el agente
agente = inicializar_agente()

# --- Gestión del Historial de Chat ---
if "mensajes" not in st.session_state:
    st.session_state.mensajes = [
        {"role": "assistant", "content": "¡Hola! Soy el asistente virtual de BimBam Buy. ¿En qué te puedo ayudar hoy con respecto a nuestras políticas y documentos?"}
    ]

# Mostrar los mensajes anteriores
for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["role"]):
        st.markdown(mensaje["content"])
        # Mostrar fuentes si existen
        if "fuentes" in mensaje and mensaje["fuentes"]:
            st.markdown("**📄 Fuentes:**")
            for fuente in mensaje["fuentes"]:
                st.markdown(f"<span class='fuente-tag'>{fuente}</span>", unsafe_allow_html=True)

# --- Entrada de Usuario ---
pregunta_usuario = st.chat_input("Escribe tu pregunta sobre BimBam Buy aquí...")

if pregunta_usuario:
    # 1. Mostrar la pregunta del usuario en la UI
    with st.chat_message("user"):
        st.markdown(pregunta_usuario)
    
    # 2. Guardar en el historial (sesión de Streamlit)
    st.session_state.mensajes.append({"role": "user", "content": pregunta_usuario})
    
    # 3. Generar y mostrar la respuesta del agente
    with st.chat_message("assistant"):
        with st.spinner("Buscando en los documentos..."):
            resultado = agente.preguntar(pregunta_usuario)
            
            respuesta_texto = resultado["respuesta"]
            fuentes = resultado["fuentes"]
            
            # Mostrar la respuesta
            st.markdown(respuesta_texto)
            
            # Mostrar fuentes
            if fuentes:
                st.markdown("**📄 Fuentes consultadas:**")
                for fuente in fuentes:
                    st.markdown(f"<span class='fuente-tag'>{fuente}</span>", unsafe_allow_html=True)
            
    # 4. Guardar la respuesta en el historial
    st.session_state.mensajes.append({
        "role": "assistant", 
        "content": respuesta_texto,
        "fuentes": fuentes
    })

# --- Barra Lateral (Sidebar) ---
with st.sidebar:
    st.header("ℹ️ Información")
    st.markdown("""
    Este asistente utiliza Inteligencia Artificial (RAG) para responder 
    preguntas basándose **únicamente** en los documentos internos de BimBam Buy.
    """)
    
    st.subheader("📚 Documentos disponibles:")
    st.markdown("""
    - Guía de Envíos
    - Manual de Garantía
    - Política de Reembolsos
    - FAQ de Métodos de Pago
    - Programa de Afiliados
    """)
    
    st.divider()
    
    st.caption("⚠️ Estás conversando con una IA.")
    
    # Botón para limpiar el chat
    if st.button("🔄 Nueva conversación", type="primary"):
        st.session_state.mensajes = [
            {"role": "assistant", "content": "¡Hola! He reiniciado nuestra conversación. ¿En qué te ayudo?"}
        ]
        agente.reiniciar_conversacion()
        st.rerun()
