"""
Módulo de carga y extracción de texto desde archivos PDF.
Corresponde a las tarjetas 1 (Colecta) y 2 (Procesamiento) del tablero Trello.

Lee todos los PDFs del directorio data/ y extrae su contenido como texto plano,
junto con metadatos como nombre del archivo y número de páginas.
"""
import os
from PyPDF2 import PdfReader
from src.config import DIRECTORIO_DATOS


def cargar_pdf(ruta_archivo: str) -> dict:
    """
    Extrae el texto completo de un archivo PDF.
    
    Args:
        ruta_archivo: Ruta absoluta al archivo PDF.
    
    Returns:
        Diccionario con el nombre del archivo, ruta, contenido y número de páginas.
    """
    lector = PdfReader(ruta_archivo)
    texto = ""

    for pagina in lector.pages:
        texto_pagina = pagina.extract_text()
        if texto_pagina:
            texto += texto_pagina + "\n"

    return {
        "nombre_archivo": os.path.basename(ruta_archivo),
        "ruta": ruta_archivo,
        "contenido": texto.strip(),
        "num_paginas": len(lector.pages),
    }


def cargar_todos_los_documentos() -> list[dict]:
    """
    Carga todos los archivos PDF del directorio de datos.
    
    Returns:
        Lista de diccionarios, cada uno con los datos de un documento.
    """
    documentos = []

    for nombre_archivo in sorted(os.listdir(DIRECTORIO_DATOS)):
        if nombre_archivo.lower().endswith(".pdf"):
            ruta = os.path.join(DIRECTORIO_DATOS, nombre_archivo)
            documento = cargar_pdf(ruta)
            documentos.append(documento)
            print(f"  ✅ {nombre_archivo} ({documento['num_paginas']} páginas)")

    return documentos


if __name__ == "__main__":
    print("📄 Cargando documentos de BimBam Buy...")
    print()
    docs = cargar_todos_los_documentos()
    print()
    print(f"Total de documentos cargados: {len(docs)}")
    for doc in docs:
        print(f"  - {doc['nombre_archivo']}: {len(doc['contenido'])} caracteres")
