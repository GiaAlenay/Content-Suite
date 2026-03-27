from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dddpy.content_log.usecase.content_log_cmd_schema import AuditResponseSchema
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.messages import HumanMessage
from dddpy.shared.langfuse_tracing.observability import audit_trace
from dddpy.brand_manual_vector.usecase.brand_manual_vector_query_usecase import (
    BrandManualVectorQueryUseCase,
)
from src.dddpy.shared.vectorize.vector_service import VectorizationService


class GovernanceAuditAgent:
    def __init__(
        self,
        vector_repo: BrandManualVectorQueryUseCase,
        vectorize_service: VectorizationService,
    ):
        # Usamos una temperatura baja (0.1 - 0.2) para que el juicio sea objetivo y no creativo
        self.llm_text = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.2)
        self.llm_vision = ChatGroq(
            model_name="llama-3.2-11b-vision-preview", temperature=0.1
        )
        self.parser = JsonOutputParser(pydantic_object=AuditResponseSchema)

        self.vector_repo = vector_repo
        self.vectorize = vectorize_service

    @audit_trace(name="Governance Agent - Audit Text Cycle")
    def audit_text_compliance(self, content_to_audit: str, brand_id: str) -> dict:
        content_vector = self.vectorize.to_vectorize_one(content_to_audit)
        relevant_rules = self.vector_repo.search_brand_context(
            brand_id=brand_id, vector=content_vector, limit=4
        )
        context_text = "\n".join([c.content_chunk for c in relevant_rules])

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "Eres un Auditor de Cumplimiento de Marca (Brand Governance Agent). "
                        "Tu trabajo es contrastar el CONTENIDO GENERADO contra las REGLAS DEL MANUAL.\n\n"
                        "REGLAS DEL MANUAL:\n{context}"
                    ),
                ),
                (
                    "user",
                    (
                        "CONTENIDO A AUDITAR:\n{content}\n\n"
                        "INSTRUCCIONES: Analiza si el contenido cumple con el tono, valores y restricciones. "
                        "Responde en JSON estricto."
                    ),
                ),
            ]
        ).partial(format_instructions=self.parser.get_format_instructions())

        chain = prompt | self.llm_text | self.parser
        return chain.invoke({"context": context_text, "content": content_to_audit})

    @audit_trace(name="Audit Text Compliance")
    def audit_text_compliance0(
        self, content_to_audit: str, brand_manual_context: str
    ) -> dict:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "Eres un Auditor de Cumplimiento de Marca (Brand Governance Agent). "
                        "Tu trabajo es contrastar el CONTENIDO GENERADO contra las REGLAS DEL MANUAL. "
                        "\n\nREGLAS DEL MANUAL:\n{context}"
                    ),
                ),
                (
                    "user",
                    (
                        "CONTENIDO A AUDITAR:\n{content}\n\n"
                        "INSTRUCCIONES: Analiza si el contenido cumple con el tono, los valores y las restricciones. "
                        "Devuelve tu respuesta en este formato JSON estricto:\n"
                        "{{\n"
                        "  'suggested_status': 'APPROVED' o 'REJECTED',\n"
                        "  'score': (número del 1 al 10),\n"
                        "  'feedback': 'Explicación breve de por qué cumple o qué reglas rompió.'\n"
                        "}}"
                    ),
                ),
            ]
        ).partial(format_instructions=self.parser.get_format_instructions())

        chain = prompt | self.llm_text | self.parser
        audit_result = chain.invoke(
            {"context": brand_manual_context, "content": content_to_audit}
        )
        return audit_result

    @audit_trace(name="Audit Image Compliance")
    def audit_image_compliance0(
        self, file_url: str, brand_manual_context: str
    ) -> AuditResponseSchema:
        system_instruction = (
            "Eres un Auditor Visual de Marca. Tu objetivo es contrastar la imagen contra el manual. "
            "Responde siguiendo estas instrucciones de formato: {format_instructions}"
        ).format(format_instructions=self.parser.get_format_instructions())

        user_content = [
            {
                "type": "text",
                "text": f"REGLAS DEL MANUAL:\n{brand_manual_context}\n\nAnaliza la imagen de la URL proporcionada.",
            },
            {
                "type": "image_url",
                "image_url": {"url": file_url},
            },
        ]

        message = HumanMessage(content=user_content)

        response = self.llm_vision.invoke(
            [
                ("system", system_instruction),
                message,
            ]
        )

        return self.parser.parse(response.content)

    @audit_trace(name="Governance Agent - Multimodal Audit")
    def audit_image_compliance(self, file_url: str, brand_id: str) -> dict:

        visual_intent = "identidad visual, colores, logo, tipografía, composición"
        query_vector = self.vectorize.to_vectorize_one(visual_intent)

        relevant_rules = self.vector_repo.search_brand_context(
            brand_id=brand_id, vector=query_vector, limit=5
        )
        brand_manual_context = "\n".join([c.content_chunk for c in relevant_rules])

        system_instruction = (
            "Eres un Auditor Visual de Marca. Tu objetivo es contrastar la IMAGEN "
            "proporcionada contra las REGLAS VISUALES del manual."
        )

        user_content = [
            {
                "type": "text",
                "text": f"REGLAS DEL MANUAL:\n{brand_manual_context}\n\nAnaliza la imagen de la URL y determina si cumple.",
            },
            {"type": "image_url", "image_url": {"url": file_url}},
        ]

        message = HumanMessage(content=user_content)
        response = self.llm_vision.invoke([("system", system_instruction), message])

        return self.parser.parse(response.content)
