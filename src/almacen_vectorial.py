"""
Módulo de almacenamiento vectorial con ChromaDB.
Corresponde a las tarjetas 3 (Indexación) y 4 (Recuperación) del tablero Trello.

Almacena los embeddings de los fragmentos de documentos en disco usando ChromaDB,
permitiendo búsquedas semánticas eficientes por similitud de coseno.
"""
import chromadb
from src.config import DIRECTORIO_CHROMA, TOP_K
from src.embeddings import ServicioEmbeddings


class AlmacenVectorial:
    """Almacén vectorial basado en ChromaDB con persistencia en disco."""

    def __init__(self):
        self.cliente = chromadb.PersistentClient(path=DIRECTORIO_CHROMA)
        self.servicio_embeddings = ServicioEmbeddings()
        self.coleccion = self.cliente.get_or_create_collection(
            name="documentos_bimbam_buy",
            metadata={"hnsw:space": "cosine"},
        )

    def indexar_fragmentos(self, fragmentos: list[dict]):
        """
        Indexa una lista de fragmentos en ChromaDB.
        Si la colección ya tiene datos, no vuelve a indexar.
        
        Args:
            fragmentos: Lista de diccionarios con id, texto y metadatos.
        """
        if self.coleccion.count() > 0:
            print(f"  ℹ️  La colección ya contiene {self.coleccion.count()} fragmentos indexados.")
            print("     Para re-indexar, elimine la carpeta chroma_db/")
            return

        textos = [f["texto"] for f in fragmentos]
        ids = [f["id"] for f in fragmentos]
        metadatos = [f["metadatos"] for f in fragmentos]

        print(f"  🔄 Generando embeddings para {len(textos)} fragmentos...")
        embeddings = self.servicio_embeddings.generar_embeddings(textos)

        # ChromaDB acepta lotes grandes, pero por seguridad usamos lotes de 500
        tamano_lote = 500
        for i in range(0, len(textos), tamano_lote):
            fin = min(i + tamano_lote, len(textos))
            self.coleccion.add(
                ids=ids[i:fin],
                documents=textos[i:fin],
                embeddings=embeddings[i:fin],
                metadatas=metadatos[i:fin],
            )

        print(f"  ✅ {len(textos)} fragmentos indexados exitosamente en ChromaDB")

    def buscar(self, consulta: str, top_k: int = TOP_K) -> list[dict]:
        """
        Busca los fragmentos más relevantes para una consulta.
        Utiliza similitud de coseno para encontrar los fragmentos más cercanos.
        
        Args:
            consulta: Texto de la pregunta del usuario.
            top_k: Número de resultados a retornar.
        
        Returns:
            Lista de diccionarios con texto, metadatos y distancia de cada resultado.
        """
        embedding_consulta = self.servicio_embeddings.generar_embedding_consulta(consulta)

        resultados = self.coleccion.query(
            query_embeddings=[embedding_consulta],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )

        coincidencias = []
        for i in range(len(resultados["documents"][0])):
            coincidencias.append({
                "texto": resultados["documents"][0][i],
                "metadatos": resultados["metadatas"][0][i],
                "distancia": resultados["distances"][0][i],
            })

        return coincidencias

    def obtener_cantidad_documentos(self) -> int:
        """Retorna la cantidad de fragmentos indexados."""
        return self.coleccion.count()


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")

    print("🗄️  Probando almacén vectorial...")
    almacen = AlmacenVectorial()
    print(f"   Fragmentos indexados: {almacen.obtener_cantidad_documentos()}")

    if almacen.obtener_cantidad_documentos() > 0:
        print()
        print("🔍 Probando búsqueda semántica...")
        consulta = "¿Cuánto tarda un envío estándar?"
        resultados = almacen.buscar(consulta)

        print(f"   Consulta: '{consulta}'")
        print(f"   Resultados encontrados: {len(resultados)}")
        for i, r in enumerate(resultados, 1):
            print(f"\n   --- Resultado {i} (distancia: {r['distancia']:.4f}) ---")
            print(f"   Fuente: {r['metadatos']['fuente']}")
            print(f"   Texto: {r['texto'][:150]}...")
