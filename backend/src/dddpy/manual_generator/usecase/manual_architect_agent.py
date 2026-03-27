from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, Any
from dddpy.shared.langfuse_tracing.observability import audit_trace


class BrandArchitectAgent:
    def __init__(self):

        self.llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.7)

    # @audit_trace(name="Generate Human Brand Manual")
    # def generate_human_manual(self, brand_name: str, raw_params: Dict[str, Any]) -> str:
    #     prompt = ChatPromptTemplate.from_messages(
    #         [
    #             (
    #                 "system",
    #                 (
    #                     "Eres un Brand DNA Architect experto. Tu objetivo es transformar parámetros brutos en un "
    #                     "Manual de Identidad de Marca robusto y estructurado en Markdown."
    #                 ),
    #             ),
    #             (
    #                 "user",
    #                 (
    #                     "Crea el Manual de Marca para: {brand_name}\n"
    #                     "Contexto inicial: {raw_params}\n\n"
    #                     "REQUISITOS DE ESTRUCTURA (USA ESTOS ENCABEZADOS):\n"
    #                     "## 1. Misión y Personalidad de Marca\n"
    #                     "## 2. Tono de Voz y Estilo de Comunicación\n"
    #                     "## 3. Reglas de Contenido (Do's and Don'ts)\n"
    #                     "## 4. Identidad Visual y Aplicación de Logo\n\n"
    #                     "INSTRUCCIÓN CRÍTICA: Sé específico. En lugar de decir 'somos amigables', di 'usamos un lenguaje "
    #                     "cercano, evitamos tecnicismos y siempre nos dirigimos al usuario como tú'. "
    #                     "Esto es vital para la futura auditoría de contenidos."
    #                 ),
    #             ),
    #         ]
    #     )
    #     chain = prompt | self.llm
    #     response = chain.invoke({"brand_name": brand_name, "raw_params": raw_params})
    #     return response.content

    @audit_trace(name="Brand Architect - Hybrid Manual Generation")
    def generate_human_manual(self, brand_name: str, raw_params: Dict[str, Any]) -> str:

        target = raw_params.get("target_audience", "Público general")
        values = ", ".join(raw_params.get("core_values", []))
        tone = raw_params.get("tone_preference", "Profesional")
        forbidden = ", ".join(raw_params.get("forbidden_topics", []))
        additional = raw_params.get(
            "additional_notes", "Sin instrucciones adicionales."
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "Eres un Brand DNA Architect de nivel Senior. Tu especialidad es destilar "
                        "visiones de negocio en reglas de comunicación accionables.\n\n"
                        "TU MISIÓN: Generar un manual en Markdown que sea la ÚNICA FUENTE DE VERDAD "
                        "para otros agentes de IA que escribirán y auditarán contenido."
                    ),
                ),
                (
                    "user",
                    (
                        "Genera el Manual de Identidad para la marca: **{brand_name}**\n\n"
                        "### DATOS ESTRUCTURADOS DEL FORMULARIO:\n"
                        "- **Audiencia Objetivo:** {target}\n"
                        "- **Valores Nucleares:** {values}\n"
                        "- **Tono Deseado:** {tone}\n"
                        "- **Restricciones/Prohibiciones:** {forbidden}\n\n"
                        "### REQUERIMIENTOS ADICIONALES DEL USUARIO:\n"
                        "{additional}\n\n"
                        "--- \n"
                        "INSTRUCCIONES DE SALIDA:\n"
                        "1. Usa encabezados ## Claros.\n"
                        "2. En la sección de 'Tono', define ejemplos de frases 'Que sí decir' vs 'Que no decir'.\n"
                        "3. Crea una sección de 'Reglas para IA' basada en las prohibiciones mencionadas.\n"
                        "4. Si el usuario dio notas adicionales, intégralas orgánicamente en la sección correspondiente."
                    ),
                ),
            ]
        )

        chain = prompt | self.llm
        response = chain.invoke(
            {
                "brand_name": brand_name,
                "target": target,
                "values": values,
                "tone": tone,
                "forbidden": forbidden,
                "additional": additional,
            }
        )

        return response.content
