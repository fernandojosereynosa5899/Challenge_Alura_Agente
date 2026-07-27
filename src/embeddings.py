"""
Módulo de generación de embeddings con OpenAI.
Corresponde a la tarjeta 3 (Indexación) del tablero Trello.

Utiliza el modelo text-embedding-3-small de OpenAI para convertir texto
en vectores numéricos que capturan su significado semántico.
"""
from openai import OpenAI
from src.config import OPENAI_API_KEY, MODELO_EMBEDDINGS


class ServicioEmbeddings:
    """Servicio de generación de embeddings usando la API de OpenAI."""

    def __init__(self):
        self.cliente = OpenAI(api_key=OPENAI_API_KEY)
        self.modelo = MODELO_EMBEDDINGS
        print(f"  🔗 Servicio de embeddings inicializado: {self.modelo}")

    def generar_embeddings(self, textos: list[str]) -> list[list[float]]:
        """
        Genera embeddings para una lista de textos.
        Procesa en lotes para respetar los límites de la API.
        
        Args:
            textos: Lista de textos a convertir en embeddings.
        
        Returns:
            Lista de vectores (embeddings), uno por cada texto.
        """
        embeddings = []
        tamano_lote = 100  # OpenAI permite hasta ~2048 textos por llamada

        for i in range(0, len(textos), tamano_lote):
            lote = textos[i : i + tamano_lote]
            respuesta = self.cliente.embeddings.create(
                model=self.modelo,
                input=lote,
            )
            embeddings_lote = [dato.embedding for dato in respuesta.data]
            embeddings.extend(embeddings_lote)

            # Progreso
            procesados = min(i + tamano_lote, len(textos))
            print(f"    Embeddings generados: {procesados}/{len(textos)}")

        return embeddings

    def generar_embedding_consulta(self, consulta: str) -> list[float]:
        """
        Genera el embedding para una consulta individual.
        
        Args:
            consulta: Texto de la pregunta del usuario.
        
        Returns:
            Vector (embedding) de la consulta.
        """
        respuesta = self.cliente.embeddings.create(
            model=self.modelo,
            input=consulta,
        )
        return respuesta.data[0].embedding


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")

    print("🔢 Probando servicio de embeddings...")
    servicio = ServicioEmbeddings()

    # Prueba con textos de ejemplo
    textos_prueba = [
        "¿Cuál es la política de reembolsos?",
        "¿Cuánto tarda un envío estándar?",
        "¿Qué cubre la garantía?",
    ]

    embeddings = servicio.generar_embeddings(textos_prueba)
    print(f"\n✅ Embeddings generados exitosamente")
    print(f"   Cantidad: {len(embeddings)}")
    print(f"   Dimensiones por vector: {len(embeddings[0])}")

    # Prueba con consulta individual
    embedding_consulta = servicio.generar_embedding_consulta("¿Cómo devuelvo un producto?")
    print(f"   Embedding de consulta: {len(embedding_consulta)} dimensiones")
