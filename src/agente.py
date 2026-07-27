"""
Agente RAG de BimBam Buy.
Corresponde a las tarjetas 4 (Recuperación) y 5 (Producción de respuestas) del tablero Trello.

Combina la búsqueda semántica en ChromaDB con el modelo de lenguaje de OpenAI
para generar respuestas fundamentadas en los documentos internos de la empresa.
"""
from openai import OpenAI
from src.config import OPENAI_API_KEY, MODELO_LLM, TEMPERATURA_LLM
from src.almacen_vectorial import AlmacenVectorial

# Prompt del sistema que define el comportamiento del agente
PROMPT_SISTEMA = """Eres el asistente virtual corporativo avanzado de BimBam Buy, una tienda en línea.
Tu rol es responder preguntas de los colaboradores basándote EXCLUSIVAMENTE en los 
documentos internos de la empresa que se te proporcionan como contexto.

REGLAS ESTRICTAS:
1. Responde SOLO con información que aparezca en el contexto proporcionado.
2. Si la información no está en el contexto, di claramente: "No encontré esta información en los manuales. Por favor, contacta a tu supervisor."
3. Responde en español, de forma clara, amable y profesional.
4. Usa un tono de soporte corporativo estándar: respetuoso, claro y directo.
5. NO inventes información. Es preferible decir "no lo sé" a dar datos incorrectos.
6. Al final de tu respuesta, propón 2 o 3 PREGUNTAS SUGERIDAS relacionadas con el tema para guiar al usuario.

Formato exacto de respuesta:
[Tu respuesta clara y directa]

💡 **Preguntas sugeridas:**
- [Pregunta 1]
- [Pregunta 2]
"""


class AgenteBimBam:
    """Agente conversacional RAG para BimBam Buy."""

    def __init__(self):
        self.cliente = OpenAI(api_key=OPENAI_API_KEY)
        self.almacen = AlmacenVectorial()
        self.historial_conversacion = []

    def _construir_contexto(self, resultados: list[dict]) -> str:
        """
        Construye el bloque de contexto a partir de los resultados de búsqueda.
        
        Args:
            resultados: Lista de fragmentos recuperados del almacén vectorial.
        
        Returns:
            Texto formateado con los fragmentos y sus fuentes.
        """
        partes = []
        for i, resultado in enumerate(resultados, 1):
            fuente = resultado["metadatos"]["fuente"]
            texto = resultado["texto"]
            partes.append(
                f"[Fragmento {i} - Fuente: {fuente}]\n{texto}"
            )
        return "\n\n---\n\n".join(partes)

    def preguntar(self, pregunta: str) -> dict:
        """
        Procesa una pregunta del usuario y genera una respuesta fundamentada.
        
        Pipeline:
        1. Busca fragmentos relevantes en ChromaDB (búsqueda semántica)
        2. Construye el contexto con los fragmentos encontrados
        3. Envía la pregunta + contexto al modelo de lenguaje
        4. Retorna la respuesta con las fuentes citadas
        
        Args:
            pregunta: Texto de la pregunta del colaborador.
        
        Returns:
            Diccionario con la respuesta, fuentes y fragmentos de contexto.
        """
        # Paso 1: Buscar fragmentos relevantes
        resultados = self.almacen.buscar(pregunta)

        # Paso 2: Construir contexto
        contexto = self._construir_contexto(resultados)

        # Paso 3: Armar el mensaje con contexto
        mensaje_usuario = f"""Contexto de documentos internos de BimBam Buy:

{contexto}

---

Pregunta del colaborador: {pregunta}"""

        # Paso 4: Preparar historial de conversación (últimos 3 turnos)
        mensajes = [{"role": "system", "content": PROMPT_SISTEMA}]
        mensajes.extend(self.historial_conversacion[-6:])
        mensajes.append({"role": "user", "content": mensaje_usuario})

        # Paso 5: Llamar al modelo de lenguaje
        respuesta = self.cliente.chat.completions.create(
            model=MODELO_LLM,
            messages=mensajes,
            temperature=TEMPERATURA_LLM,
            max_tokens=1000,
        )

        texto_respuesta = respuesta.choices[0].message.content

        # Paso 6: Actualizar historial de conversación
        self.historial_conversacion.append(
            {"role": "user", "content": pregunta}
        )
        self.historial_conversacion.append(
            {"role": "assistant", "content": texto_respuesta}
        )

        # Paso 7: Extraer fuentes únicas
        fuentes = list(set(
            r["metadatos"]["fuente"] for r in resultados
        ))

        return {
            "respuesta": texto_respuesta,
            "fuentes": fuentes,
            "fragmentos_contexto": resultados,
        }

    def reiniciar_conversacion(self):
        """Reinicia el historial de conversación para una nueva sesión."""
        self.historial_conversacion = []


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")

    print("🤖 Iniciando Agente BimBam Buy...")
    print()
    agente = AgenteBimBam()

    preguntas_prueba = [
        "¿Cuánto tarda un envío estándar?",
        "¿Cómo solicito un reembolso?",
        "¿Qué métodos de pago aceptan?",
    ]

    for pregunta in preguntas_prueba:
        print(f"❓ Pregunta: {pregunta}")
        print("-" * 60)
        resultado = agente.preguntar(pregunta)
        print(f"💬 Respuesta: {resultado['respuesta']}")
        print(f"📄 Fuentes: {resultado['fuentes']}")
        print("=" * 60)
        print()
