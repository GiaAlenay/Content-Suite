from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dddpy.content_log.usecase.content_log_cmd_schema import AuditResponseSchema
from langchain_core.output_parsers import JsonOutputParser
import base64
from langchain_core.messages import HumanMessage


class GovernanceService:
    def __init__(self):
        # Usamos una temperatura baja (0.1 - 0.2) para que el juicio sea objetivo y no creativo
        self.llm_text = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.2)
        self.llm_vision = ChatGroq(
            model_name="llama-3.2-11b-vision-preview", temperature=0.1
        )
        self.parser = JsonOutputParser(pydantic_object=AuditResponseSchema)

    def audit_text_compliance(
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

    def audit_image_compliance(
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
