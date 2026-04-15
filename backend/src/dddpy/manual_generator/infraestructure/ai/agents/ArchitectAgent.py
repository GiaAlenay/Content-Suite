from langchain_core.prompts import ChatPromptTemplate


class ArchitectAgent:
    def __init__(self, llm):
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "Eres un Senior Brand DNA Architect. Tu especialidad es transformar visiones abstractas "
                        "en manuales de identidad técnica y emocionalmente precisos.\n\n"
                        "TU OBJETIVO: Crear un manual en Markdown que sirva como 'Constitución' para la marca. "
                        "Debe ser lo suficientemente detallado para que otros agentes del sistema operen bajo estos lineamientos "
                        "sin desviarse de la esencia de la marca."
                    ),
                ),
                (
                    "user",
                    (
                        "### 1. IDENTIDAD BASE DE LA MARCA (NO NEGOCIABLE):\n"
                        "Nombre: {brand_name}\n"
                        "Descripción: {brand_description}\n\n"
                        "### 2. PARÁMETROS DETALLADOS:\n"
                        "- Audiencia Objetivo: {target}\n"
                        "- Valores Core: {values}\n"
                        "- Tono de Voz: {tone}\n"
                        "- Prohibiciones/Restricciones: {forbidden}\n"
                        "- Notas Adicionales: {additional}\n\n"
                        "### 3. IDENTIDAD VISUAL:\n"
                        "- Estilo Visual: {visual_style}\n"
                        "- Paleta de Colores: {colors}\n"
                        "- Reglas de Logo: {logo_rules}\n\n"
                        "--- \n"
                        "INSTRUCCIONES DE CONSTRUCCIÓN:\n"
                        "1. **Síntesis**: Integra la descripción base con los nuevos requerimientos priorizando la coherencia de marca.\n"
                        "2. **Sección de Tono**: Crea una tabla de 'Voz de la Marca' con ejemplos de 'Cómo hablar' vs 'Cómo NO hablar'.\n"
                        "3. **Reglas para IA**: Define explícitamente cómo debe comportarse un agente del sistema al redactar para esta marca.\n"
                        "4. **Formato**: Usa Markdown profesional, con negritas, listas y encabezados ## y ###.\n"
                        "5. SECCIÓN VISUAL TÉCNICA: Crea una sección llamada '## Lineamientos Visuales'.\n"
                        "   - Define los códigos Hexadecimales de los colores proporcionados.\n"
                        "   - Escribe reglas explícitas de 'Uso de Logo' (ej: tamaño mínimo, fondos permitidos).\n"
                        "   - Describe el estilo fotográfico permitido.\n"
                        "   *IMPORTANTE*: Redacta esto de forma que una IA de visión pueda usar estas reglas para auditar una imagen."
                    ),
                ),
            ]
        )

    async def execute(
        self, brand_name: str, brand_description: str, raw_params: dict
    ) -> str:

        target = raw_params.get("target_audience", "Público general")
        values = ", ".join(raw_params.get("core_values", []))
        tone = raw_params.get("tone_preference", "Profesional")
        forbidden = ", ".join(raw_params.get("forbidden_topics", []))
        additional = raw_params.get("additional_notes", "Sin notas adicionales.")
        colors = ", ".join(raw_params.get("brand_colors", []))
        visual_style = raw_params.get("visual_style", "No especificado")
        logo_rules = raw_params.get(
            "logo_guidelines", "Seguir estándares de legibilidad"
        )

        chain = self.prompt | self.llm
        response = await chain.ainvoke(
            {
                "brand_name": brand_name,
                "brand_description": brand_description,
                "target": target,
                "values": values,
                "tone": tone,
                "forbidden": forbidden,
                "additional": additional,
                "visual_identity": f"REGLAS VISUALES:\n- Colores: {colors}\n- Estilo: {visual_style}\n- Logo: {logo_rules}",
            }
        )
        return response.content
