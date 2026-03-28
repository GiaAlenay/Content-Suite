from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, Any, Optional, List
from dddpy.shared.langfuse_tracing.observability import audit_trace


class BrandArchitectAgent:
    def __init__(self):

        self.llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.7)


class BrandArchitectAgent:
    def __init__(self):
        # Mantenemos temperatura 0.7 para que el manual sea creativo y bien redactado
        self.llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.7)

    @audit_trace(name="Brand Architect - Contextual Manual Generation")
    def generate_human_manual(
        self,
        brand_name: str,
        raw_params: Dict[str, Any],
        brand_description: Optional[str],
        audit_feedback: Optional[List[str]] = None,
    ) -> str:

        # Limpieza de inputs
        target = raw_params.get("target_audience", "Público general")
        values = ", ".join(raw_params.get("core_values", []))
        tone = raw_params.get("tone_preference", "Profesional")
        forbidden = ", ".join(raw_params.get("forbidden_topics", []))
        additional = raw_params.get("additional_notes", "Sin notas adicionales.")

        feedback_str = (
            "\n".join([f"- {f}" for f in audit_feedback])
            if audit_feedback
            else "Ninguna observación."
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "Eres un Senior Brand DNA Architect. Tu especialidad es transformar visiones abstractas "
                        "en manuales de identidad técnica y emocionalmente precisos.\n\n"
                        "TU OBJETIVO: Crear un manual en Markdown que sirva como 'Constitución' para la marca. "
                        "Debe ser lo suficientemente detallado para que otros agentes de IA operen bajo estos lineamientos "
                        "sin desviarse de la esencia de la marca."
                    ),
                ),
                (
                    "user",
                    (
                        "### 1. IDENTIDAD BASE DE LA MARCA (NO NEGOCIABLE):\n"
                        "Nombre: {brand_name}\n"
                        "Descripción: {brand_description}\n\n"
                        "### 2. NUEVOS REQUERIMIENTOS DEL USUARIO:\n"
                        "- Audiencia: {target}\n"
                        "- Valores: {values}\n"
                        "- Tono deseado: {tone}\n"
                        "- Prohibiciones: {forbidden}\n"
                        "- Notas extra: {additional}\n\n"
                        "### 3. OBSERVACIONES DEL AUDITOR DE GOBERNANZA:\n"
                        "{audit_feedback}\n\n"
                        "--- \n"
                        "INSTRUCCIONES DE CONSTRUCCIÓN:\n"
                        "1. **Síntesis**: Integra la descripción base con los nuevos requerimientos. Si el auditor señaló conflictos, "
                        "resuelve la tensión priorizando la coherencia de marca.\n"
                        "2. **Sección de Tono**: Crea una tabla de 'Voz de la Marca' con ejemplos de 'Cómo hablar' vs 'Cómo NO hablar'.\n"
                        "3. **Reglas para IA**: Define explícitamente cómo debe comportarse un agente de IA al redactar para esta marca.\n"
                        "4. **Formato**: Usa Markdown profesional, con negritas, listas y encabezados ## y ###.\n"
                        "5. **Personalidad**: Si el feedback del auditor sugirió mejoras de tono, aplícalas aquí."
                    ),
                ),
            ]
        )

        chain = prompt | self.llm

        response = chain.invoke(
            {
                "brand_name": brand_name,
                "brand_description": brand_description or "No proporcionada.",
                "target": target,
                "values": values,
                "tone": tone,
                "forbidden": forbidden,
                "additional": additional,
                "audit_feedback": feedback_str,
            }
        )

        return response.content

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
