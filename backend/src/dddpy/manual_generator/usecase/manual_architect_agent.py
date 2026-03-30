from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, Any, Optional, List
from dddpy.shared.langfuse_tracing.observability import audit_trace


class BrandArchitectAgent:
    def __init__(self):
        self.llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.7)

    # @audit_trace(name="Brand Architect - Contextual Manual Generation")
    def generate_human_manual(
        self,
        brand_name: str,
        raw_params: Dict[str, Any],
        brand_description: Optional[str],
        audit_feedback: Optional[List[str]] = None,
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
                        "Debe ser lo suficientemente detallado para que otros agentesdel sistema operen bajo estos lineamientos "
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
                        "- Identidad visual: {visual_identity}\n"
                        "- Prohibiciones: {forbidden}\n"
                        "- Notas extra: {additional}\n\n"
                        "### 3. OBSERVACIONES DEL AUDITOR DE GOBERNANZA:\n"
                        "{audit_feedback}\n\n"
                        "--- \n"
                        "INSTRUCCIONES DE CONSTRUCCIÓN:\n"
                        "1. **Síntesis**: Integra la descripción base con los nuevos requerimientos. Si el auditor señaló conflictos, "
                        "resuelve la tensión priorizando la coherencia de marca.\n"
                        "2. **Sección de Tono**: Crea una tabla de 'Voz de la Marca' con ejemplos de 'Cómo hablar' vs 'Cómo NO hablar'.\n"
                        "3. **Reglas para IA**: Define explícitamente cómo debe comportarse un agentedel sistema al redactar para esta marca.\n"
                        "4. **Formato**: Usa Markdown profesional, con negritas, listas y encabezados ## y ###.\n"
                        "5. **Personalidad**: Si el feedback del auditor sugirió mejoras de tono, aplícalas aquí.\n"
                        "6. SECCIÓN VISUAL TÉCNICA: Crea una sección llamada '## Lineamientos Visuales'.\n"
                        "   - Define los códigos Hexadecimales de los colores proporcionados.\n"
                        "   - Escribe reglas explícitas de 'Uso de Logo' (ej: tamaño mínimo, fondos permitidos).\n"
                        "   - Describe el estilo fotográfico permitido.\n"
                        "   *IMPORTANTE*: Redacta esto de forma que una IA de visión pueda usar estas reglas para auditar una imagen."
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
                "visual_identity": f"REGLAS VISUALES:\n- Colores: {colors}\n- Estilo: {visual_style}\n- Logo: {logo_rules}",
                "audit_feedback": feedback_str,
            }
        )

        return response.content

    # @audit_trace(name="Brand Architect - Manual Refinement")
    def refine_manual(
        self,
        current_content: str,
        refinement_instructions: str,
        brand_name: str,
        audit_feedback: List[str] = [],
    ) -> str:
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
                        "Eres un Editor Senior de Identidad de Marca. Tu tarea es MODIFICAR un manual existente "
                        "siguiendo las instrucciones precisas del usuario, manteniendo la coherencia con el resto del documento."
                        "REGLAS DE PRIORIDAD:\n"
                        "1. La ESENCIA BASE de la marca es sagrada.\n"
                        "2. Las instrucciones del usuario son tu guía de cambio.\n"
                        "3. Si el auditor detectó conflictos, debes resolver la edición de forma que se mitiguen esos riesgos."
                    ),
                ),
                (
                    "user",
                    (
                        "MARCA: {brand_name}\n\n"
                        "### OBSERVACIONES DEL AUDITOR:\n{audit_feedback}\n\n"
                        "### CONTENIDO ACTUAL DEL MANUAL:\n"
                        "{current_content}\n\n"
                        "### INSTRUCCIONES DE AJUSTE:\n"
                        "{instructions}\n\n"
                        "--- \n"
                        "REGLAS DE EDICIÓN:\n"
                        "1. Mantén la estructura Markdown original.\n"
                        "2. Solo cambia las secciones afectadas por las instrucciones.\n"
                        "3. Asegúrate de que el tono general siga siendo profesional.\n"
                        "4. Devuelve el manual COMPLETO con los cambios aplicados."
                    ),
                ),
            ]
        )

        chain = prompt | self.llm
        response = chain.invoke(
            {
                "brand_name": brand_name,
                "current_content": current_content,
                "instructions": refinement_instructions,
                "audit_feedback": feedback_str,
            }
        )

        return response.content

    # # @audit_trace(name="Generate Human Brand Manual")
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
