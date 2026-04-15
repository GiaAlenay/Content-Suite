import re
from typing import List, Dict


def split_content_into_sections(full_content: str) -> List[Dict]:
    """
    Parsea un string Markdown y lo divide en secciones basadas en encabezados (##).
    Retorna una lista de diccionarios compatibles con CreateManualSectionSchema.
    """
    # Buscamos encabezados de nivel 2 (## Nombre de la Sección)
    # El regex captura el nombre y todo el contenido hasta el siguiente encabezado
    pattern = r"##\s*(?P<name>.*?)\n(?P<content>.*?)(?=\n##|$)"

    # flags=re.DOTALL permite que el '.' capture saltos de línea
    matches = re.finditer(pattern, full_content, re.DOTALL)

    sections = []
    for i, match in enumerate(matches, start=1):
        name = match.group("name").strip()
        content = match.group("content").strip()

        sections.append({"section_name": name, "content": content, "order_number": i})

    # Caso de respaldo: Si la IA no generó encabezados ##,
    # guardamos todo como una sección única para no perder datos.
    if not sections:
        sections.append(
            {
                "section_name": "Contenido General",
                "content": full_content.strip(),
                "order_number": 1,
            }
        )

    return sections
