from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dddpy.shared.langfuse_tracing.observability import audit_trace
from dddpy.shared.vectorize.vector_service import VectorizationService
from dddpy.brand_manual_vector.usecase.brand_manual_vector_query_usecase import (
    BrandManualVectorQueryUseCase,
)
from langchain_core.output_parsers import JsonOutputParser
import json
from typing import Optional

from dddpy.content_log.usecase.content_log_cmd_schema import GeneratedContentSchema


class CreativeEngineAgent:
    def __init__(
        self,
        vector_repo: BrandManualVectorQueryUseCase,
        vectorize_service: VectorizationService,
    ):
        self.llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.7)
        self.vector_repo = vector_repo
        self.vectorize = vectorize_service
        self.content_parser = JsonOutputParser(pydantic_object=GeneratedContentSchema)

    def generate_content(
        self,
        user_prompt: str,
        brand_name: str,
        brand_description: Optional[str],
        brand_id: str,
        content_type: str,
        history_content: str = None,
    ) -> GeneratedContentSchema:

        query_vector = self.vectorize.to_vectorize_one(user_prompt)
        relevant_chunks = self.vector_repo.search_brand_context(
            brand_id=brand_id, vector=query_vector
        )

        context_text = "\n".join([chunk.content_chunk for chunk in relevant_chunks])
        if not context_text:
            context_text = "No se encontraron reglas específicas en el manual para este tema. Cíñete estrictamente a la descripción base."

        refinement_instruction = ""
        if history_content:
            refinement_instruction = (
                f"\n### CONTEXTO DE REFINAMIENTO:\n"
                f"El usuario pide un ajuste sobre: '{history_content}'\n"
                f"Modifica el contenido anterior siguiendo el nuevo pedido, manteniendo la esencia."
            )

        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Eres el Director Creativo y Copywriter Senior de la marca **{brand_name}**.
                    
                    ### IDENTIDAD INNEGOCIABLE DE LA MARCA:
                    {brand_description}
                    
                    ### CONTEXTO ADICIONAL (MANUAL DE MARCA):
                    {context}
                    
                    ### REGLAS DE ORO DE REDACCIÓN:
                    1. NUNCA inventes servicios, productos o sectores que no estén en la Identidad o el Manual.
                    2. Si el pedido del usuario parece ajeno a la marca (ej. mascotas en una cafetería), NO rechaces la solicitud. En su lugar, actúa como un Director Creativo: busca un "puente creativo" que conecte el pedido con la esencia de {brand_name}. 
                    (Ejemplo: "Celebramos el día del mejor amigo con un café que te acompaña en tus paseos"). 
                    Solo rechaza y explica si el pedido es explícitamente dañino, ilegal o rompe totalmente los valores éticos de la marca.
                    3. Si el pedido es totalmente imposible de vincular o contradice los valores éticos, usa 'is_aligned: false' y explica por qué en 'llm_opinion'.
                    4. Mantén siempre el tono definido en el manual.
                    {refinement_logic}
                    
                    ### FORMATO DE SALIDA (OBLIGATORIO):
                    Debes responder ÚNICAMENTE con un objeto JSON válido con la siguiente estructura:
                    {{
                        "llm_opinion": "Tu explicación técnica o justificación de por qué el contenido es así o por qué se cambió el enfoque debido a la identidad de marca.",
                        "generated_content": "El contenido puro (post, artículo, etc.) listo para ser publicado.",
                        "is_aligned": "true si el pedido se pudo integrar naturalmente, false si el puente creativo fue forzado o muy alejado."
                    }}
                    
                    """,
                ),
                (
                    "user",
                    "Formato solicitado: {content_type}\nIndicación del usuario: {user_prompt}",
                ),
            ]
        ).partial(format_instructions=self.content_parser.get_format_instructions())

        chain = prompt_template | self.llm | self.content_parser
        return chain.invoke(
            {
                "brand_name": brand_name,
                "brand_description": brand_description or "No proporcionada.",
                "context": context_text or "No hay reglas específicas.",
                "content_type": content_type,
                "user_prompt": user_prompt,
                "refinement_logic": refinement_instruction,
            }
        )
