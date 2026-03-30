from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dddpy.content_log.usecase.content_log_cmd_schema import (
    AuditResponseSchema,
    AuditPromptSchema,
)
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.messages import HumanMessage
from dddpy.shared.langfuse_tracing.observability import audit_trace
from dddpy.brand_manual_vector.usecase.brand_manual_vector_query_usecase import (
    BrandManualVectorQueryUseCase,
)
from dddpy.shared.vectorize.vector_service import VectorizationService


class GovernanceAuditAgent:
    def __init__(
        self,
        vector_repo: BrandManualVectorQueryUseCase,
        vectorize_service: VectorizationService,
    ):
        self.llm_text = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.2)
        self.llm_vision = ChatGroq(
            model_name="llama-3.2-11b-vision-preview", temperature=0.1
        )
        self.audit_content_parser = JsonOutputParser(
            pydantic_object=AuditResponseSchema
        )
        self.prompt_parser = JsonOutputParser(pydantic_object=AuditPromptSchema)

        self.vector_repo = vector_repo
        self.vectorize = vectorize_service

    # @audit_trace(name="Creative Engine - Prompt Pre-Audit")
    def audit_user_request(
        self, brand_id: str, user_prompt: str, target_content: str
    ) -> dict:
        query_vector = self.vectorize.to_vectorize_one(user_prompt)
        relevant_rules = self.vector_repo.search_brand_context(
            brand_id=brand_id, vector=query_vector, limit=6
        )
        brand_context = "\n".join([c.content_chunk for c in relevant_rules])

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "Eres un Director Creativo y Guardián de Marca Senior.\n"
                        "Tu misión es auditar el PROMPT del usuario antes de enviarlo al motor de generación final.\n\n"
                        "### CONTEXTO DEL MANUAL DE MARCA:\n{context}\n\n"
                        "### TAREAS DE AUDITORÍA:\n"
                        "1. **Validación de Intención**: Compara el 'TIPO ESPERADO' ({target}) con el texto del usuario. "
                        "Si el usuario seleccionó 'Guion' pero pide 'una tabla de Excel', marca is_type_match = false.\n"
                        "2. **Filtro de Gobernanza**: Identifica si el prompt pide violar reglas del manual "
                        "(ej: usar colores prohibidos, tonos no permitidos o temas restringidos).\n"
                        "3. **Análisis de Calidad**: Si el prompt es pobre ('haz un post'), genera un 'improved_prompt' "
                        "que incluya contexto de la marca, estructura profesional y técnica adecuada para el tipo de contenido.\n"
                        "4. **Severidad**: HIGH si hay una contradicción directa con el manual o un error de tipo crítico. "
                        "LOW si el prompt es válido pero puede mejorarse.\n\n"
                        "{format_instructions}"
                    ),
                ),
                (
                    "user",
                    (
                        "### DATOS DE ENTRADA:\n"
                        "- TIPO SELECCIONADO POR USUARIO: '{target}'\n"
                        "- PROMPT ESCRITO: '{user_prompt}'"
                    ),
                ),
            ]
        ).partial(format_instructions=self.prompt_parser.get_format_instructions())

        chain = prompt | self.llm_text | self.prompt_parser

        return chain.invoke(
            {
                "context": brand_context,
                "user_prompt": user_prompt,
                "target": target_content,
            }
        )

    # @audit_trace(name="Governance Agent - Audit Text Compliance")
    def audit_text_compliance(self, content_to_audit: str, brand_id: str) -> dict:
        content_vector = self.vectorize.to_vectorize_one(content_to_audit)
        relevant_rules = self.vector_repo.search_brand_context(
            brand_id=brand_id,
            vector=content_vector,
            limit=6,
        )
        context_text = "\n".join([c.content_chunk for c in relevant_rules])

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "Eres un Auditor de Cumplimiento de Marca de élite. Tu función es contrastar "
                        "el CONTENIDO GENERADO contra la 'Constitución' de la marca.\n\n"
                        "### REGLAS DEL MANUAL:\n{context}\n\n"
                        "### CRITERIOS DE EVALUACIÓN:\n"
                        "1. **Tono y Voz**: ¿Coincide con la preferencia de tono establecida?\n"
                        "2. **Audiencia**: ¿El lenguaje es adecuado para el target_audience definido?\n"
                        "3. **Temas Prohibidos**: ¿Se menciona algún forbidden_topic o concepto sensible?\n"
                        "4. **Valores**: ¿El mensaje refuerza los core_values de la marca?\n"
                        "5. **Coherencia**: ¿Las instrucciones especiales (additional_notes) se están respetando?\n\n"
                        "{format_instructions}"
                    ),
                ),
                (
                    "user",
                    (
                        "CONTENIDO A AUDITAR:\n{content}\n\n"
                        "Analiza rigurosamente y genera el reporte de cumplimiento en JSON."
                    ),
                ),
            ]
        ).partial(
            format_instructions=self.audit_content_parser.get_format_instructions()
        )

        chain = prompt | self.llm_text | self.audit_content_parser
        return chain.invoke({"context": context_text, "content": content_to_audit})

    # @audit_trace(name="Governance Agent - Multimodal Visual Audit")
    def audit_image_compliance(self, file_url: str, brand_id: str) -> dict:
        # Buscamos específicamente reglas visuales en el vector store
        visual_intent = (
            "colores marca HEX, estilo visual, logo, tipografía, composición, estética"
        )
        query_vector = self.vectorize.to_vectorize_one(visual_intent)

        relevant_rules = self.vector_repo.search_brand_context(
            brand_id=brand_id, vector=query_vector, limit=6
        )
        brand_manual_context = "\n".join([c.content_chunk for c in relevant_rules])

        system_instruction = (
            "Eres un Auditor Visual de Marca con ojo clínico. Tu misión es validar si la IMAGEN "
            "cumple con los lineamientos visuales técnicos y estratégicos del manual.\n\n"
            "### REGLAS VISUALES DEL MANUAL:\n"
            f"{brand_manual_context}\n\n"
            "### PUNTOS DE CONTROL CRÍTICOS:\n"
            "1. **Paleta de Colores (HEX)**: ¿Aparecen los colores de la marca? ¿Los colores presentes chocan con la identidad?\n"
            "2. **Estilo Visual**: ¿La imagen es coherente con la descripción de visual_style (ej: minimalista, rústico, etc.)?\n"
            "3. **Uso del Logo**: Si hay un logo, ¿respeta las logo_guidelines (áreas de protección, fondos permitidos)?\n"
            "4. **Audiencia**: ¿La composición y el sujeto de la imagen apelan al target_audience?\n"
            "5. **Calidad y Composición**: ¿Refleja el nivel de calidad exigido en las notas adicionales?"
        )

        user_content = [
            {
                "type": "text",
                "text": (
                    "Analiza la imagen de la URL proporcionada bajo el estándar de JSON estricto. "
                    "Si hay desviaciones en los códigos de color o estilo visual, detállalas en el feedback."
                ),
            },
            {"type": "image_url", "image_url": {"url": file_url}},
        ]

        # Invocación directa para visión
        message = HumanMessage(content=user_content)
        response = self.llm_vision.invoke([("system", system_instruction), message])

        # Aseguramos que el parseo sea limpio
        return self.audit_content_parser.parse(response.content)
