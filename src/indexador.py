"""
Script de indexación: ejecutar una vez para procesar los PDFs y crear la base vectorial.
Corresponde a las tarjetas 1, 2 y 3 del tablero Trello.

Este script orquesta todo el pipeline de preparación de datos:
1. Cargar los PDFs del directorio data/
2. Limpiar y fragmentar el texto en chunks
3. Generar embeddings y almacenarlos en ChromaDB
"""
from src.cargador_documentos import cargar_todos_los_documentos
from src.procesador_texto import procesar_documentos
from src.almacen_vectorial import AlmacenVectorial


def ejecutar_indexacion():
    """
    Ejecuta el pipeline completo de indexación.
    Solo necesita ejecutarse una vez (o cuando se actualicen los documentos).
    
    Returns:
        Lista de fragmentos procesados.
    """
    print("🚀 Iniciando indexación de documentos BimBam Buy...")
    print()

    # Paso 1: Cargar los PDFs
    print("📄 Paso 1: Cargando documentos desde data/...")
    documentos = cargar_todos_los_documentos()
    print(f"   Documentos cargados: {len(documentos)}")
    print()

    # Paso 2: Procesar y fragmentar el texto
    print("✂️  Paso 2: Procesando y fragmentando textos...")
    fragmentos = procesar_documentos(documentos)
    print(f"   Total de fragmentos generados: {len(fragmentos)}")
    print()

    # Paso 3: Generar embeddings e indexar en ChromaDB
    print("🔢 Paso 3: Generando embeddings e indexando en ChromaDB...")
    almacen = AlmacenVectorial()
    almacen.indexar_fragmentos(fragmentos)
    print()

    print("=" * 60)
    print("✅ ¡Indexación completada exitosamente!")
    print(f"   Documentos procesados: {len(documentos)}")
    print(f"   Fragmentos indexados: {almacen.obtener_cantidad_documentos()}")
    print("=" * 60)

    return fragmentos


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    ejecutar_indexacion()
