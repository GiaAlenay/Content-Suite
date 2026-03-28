from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dddpy.shared.langfuse_tracing.observability import audit_trace
from dddpy.shared.vectorize.vector_service import VectorizationService
from dddpy.brand_manual_vector.usecase.brand_manual_vector_query_usecase import (
    BrandManualVectorQueryUseCase,
)


class CreativeEngineAgent:
    def __init__(
        self,
        vector_repo: BrandManualVectorQueryUseCase,
        vectorize_service: VectorizationService,
    ):
        self.llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.7)
        self.vector_repo = vector_repo
        self.vectorize = vectorize_service

    # @audit_trace(name="Generate Content with RAG")
    # def generate_content_with_rag(
    #     self, user_prompt: str, brand_name: str, context_chunks: str, content_type: str
    # ) -> str:
    #     prompt_template = ChatPromptTemplate.from_messages(
    #         [
    #             (
    #                 "system",
    #                 (
    #                     "Eres un Redactor Creativo experto para la marca {brand_name}. "
    #                     "Tu misión es generar contenido que respete estrictamente el ADN de la marca. "
    #                     "\n\nREGLAS DE ORO (Extraídas del Manual):\n{context}"
    #                 ),
    #             ),
    #             ("user", "Tipo de contenido: {content_type}\nPedido: {user_prompt}"),
    #         ]
    #     )

    #     chain = prompt_template | self.llm
    #     response = chain.invoke(
    #         {
    #             "brand_name": brand_name,
    #             "context": context_chunks,
    #             "content_type": content_type,
    #             "user_prompt": user_prompt,
    #         }
    #     )
    #     return response.content

    @audit_trace(name="Creative Agent - Autonomous RAG")
    def generate_content(
        self, user_prompt: str, brand_name: str, brand_id: str, content_type: str
    ) -> str:
        # EL AGENTE DECIDE BUSCAR SU CONTEXTO (Esto es RAG real)
        query_vector = self.vectorize.to_vectorize_one(user_prompt)
        relevant_chunks = self.vector_repo.search_brand_context(
            brand_id=brand_id, vector=query_vector
        )

        context_text = "\n".join([chunk.content_chunk for chunk in relevant_chunks])

        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Eres un Redactor Creativo experto para {brand_name}. Reglas: {context}",
                ),
                ("user", "Tipo: {content_type}\nPedido: {user_prompt}"),
            ]
        )

        chain = prompt_template | self.llm
        response = chain.invoke(
            {
                "brand_name": brand_name,
                "context": context_text,
                "content_type": content_type,
                "user_prompt": user_prompt,
            }
        )
        return response.content
