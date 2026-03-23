from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, Any


class CreativeEngineService:
    def __init__(self):
        # Llama-3.3-70b es perfecto para seguir reglas de marca
        self.llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.7)

    def generate_content_with_rag(
        self, user_prompt: str, brand_name: str, context_chunks: str, content_type: str
    ) -> str:
        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "Eres un Redactor Creativo experto para la marca {brand_name}. "
                        "Tu misión es generar contenido que respete estrictamente el ADN de la marca. "
                        "\n\nREGLAS DE ORO (Extraídas del Manual):\n{context}"
                    ),
                ),
                ("user", "Tipo de contenido: {content_type}\nPedido: {user_prompt}"),
            ]
        )

        chain = prompt_template | self.llm
        response = chain.invoke(
            {
                "brand_name": brand_name,
                "context": context_chunks,
                "content_type": content_type,
                "user_prompt": user_prompt,
            }
        )
        return response.content
