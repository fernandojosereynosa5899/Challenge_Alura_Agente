"""
Módulo de procesamiento y fragmentación (chunking) de texto.
Corresponde a la tarjeta 2 (Procesamiento y Extracción) del tablero Trello.

Toma el texto extraído de los documentos, lo limpia y lo divide en fragmentos
(chunks) con solapamiento para mantener el contexto entre ellos.
"""
import re
from src.config import TAMANO_CHUNK, SOLAPAMIENTO_CHUNK


def limpiar_texto(texto: str) -> str:
    """
    Limpia el texto extraído de los PDFs.
    Elimina caracteres problemáticos, normaliza espacios y saltos de línea.
    
    Args:
        texto: Texto sin procesar extraído del PDF.
    
    Returns:
        Texto limpio y normalizado.
    """
    # Eliminar caracteres nulos
    texto = texto.replace("\x00", "")
    # Normalizar espacios múltiples a uno solo
    texto = re.sub(r" {2,}", " ", texto)
    # Normalizar saltos de línea excesivos
    texto = re.sub(r"\n{3,}", "\n\n", texto)
    return texto.strip()


def fragmentar_texto(
    texto: str,
    tamano: int = TAMANO_CHUNK,
    solapamiento: int = SOLAPAMIENTO_CHUNK,
) -> list[str]:
    """
    Divide el texto en fragmentos (chunks) con solapamiento.
    Intenta cortar en límites naturales como párrafos, oraciones o comas.
    
    Args:
        texto: Texto limpio a fragmentar.
        tamano: Tamaño máximo de cada fragmento en caracteres.
        solapamiento: Caracteres de solapamiento entre fragmentos consecutivos.
    
    Returns:
        Lista de fragmentos de texto.
    """
    texto = limpiar_texto(texto)
    fragmentos = []
    inicio = 0

    while inicio < len(texto):
        fin = inicio + tamano

        # Si no estamos al final del texto, buscar un punto de corte natural
        if fin < len(texto):
            for separador in ["\n\n", "\n", ". ", ", "]:
                ultimo_separador = texto.rfind(separador, inicio, fin)
                if ultimo_separador > inicio:
                    fin = ultimo_separador + len(separador)
                    break

        fragmento = texto[inicio:fin].strip()
        if fragmento:
            fragmentos.append(fragmento)

        # Avanzar con solapamiento para no perder contexto
        inicio = fin - solapamiento

    return fragmentos


def procesar_documentos(documentos: list[dict]) -> list[dict]:
    """
    Procesa una lista de documentos: limpia texto y genera fragmentos con metadatos.
    Cada fragmento incluye un ID único y la referencia al documento de origen.
    
    Args:
        documentos: Lista de diccionarios con los datos de cada documento.
    
    Returns:
        Lista de fragmentos, cada uno con su texto y metadatos asociados.
    """
    todos_los_fragmentos = []

    for documento in documentos:
        fragmentos = fragmentar_texto(documento["contenido"])

        for indice, fragmento in enumerate(fragmentos):
            todos_los_fragmentos.append({
                "id": f"{documento['nombre_archivo']}__fragmento_{indice}",
                "texto": fragmento,
                "metadatos": {
                    "fuente": documento["nombre_archivo"],
                    "indice_fragmento": indice,
                    "total_fragmentos": len(fragmentos),
                },
            })

    return todos_los_fragmentos


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    
    from src.cargador_documentos import cargar_todos_los_documentos

    print("📄 Cargando documentos...")
    documentos = cargar_todos_los_documentos()
    print()

    print("✂️  Procesando y fragmentando textos...")
    fragmentos = procesar_documentos(documentos)
    print(f"   Total de fragmentos generados: {len(fragmentos)}")
    print()

    # Mostrar resumen por documento
    from collections import Counter
    conteo = Counter(f["metadatos"]["fuente"] for f in fragmentos)
    for fuente, cantidad in conteo.items():
        print(f"  📄 {fuente}: {cantidad} fragmentos")

    print()
    print("Ejemplo de fragmento:")
    print(f"  ID: {fragmentos[0]['id']}")
    print(f"  Texto (primeros 200 chars): {fragmentos[0]['texto'][:200]}...")
