from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, Any
from dddpy.shared.langfuse_tracing.observability import audit_trace


class BrandManualGeneratorService:
    def __init__(self):

        self.llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.7)

    @audit_trace(name="Generate Human Brand Manual")
    def generate_human_manual(self, brand_name: str, raw_params: Dict[str, Any]) -> str:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "Eres un Brand DNA Architect experto. Tu objetivo es transformar parámetros brutos en un "
                        "Manual de Identidad de Marca robusto y estructurado en Markdown."
                    ),
                ),
                (
                    "user",
                    (
                        "Crea el Manual de Marca para: {brand_name}\n"
                        "Contexto inicial: {raw_params}\n\n"
                        "REQUISITOS DE ESTRUCTURA (USA ESTOS ENCABEZADOS):\n"
                        "## 1. Misión y Personalidad de Marca\n"
                        "## 2. Tono de Voz y Estilo de Comunicación\n"
                        "## 3. Reglas de Contenido (Do's and Don'ts)\n"
                        "## 4. Identidad Visual y Aplicación de Logo\n\n"
                        "INSTRUCCIÓN CRÍTICA: Sé específico. En lugar de decir 'somos amigables', di 'usamos un lenguaje "
                        "cercano, evitamos tecnicismos y siempre nos dirigimos al usuario como tú'. "
                        "Esto es vital para la futura auditoría de contenidos."
                    ),
                ),
            ]
        )
        chain = prompt | self.llm
        response = chain.invoke({"brand_name": brand_name, "raw_params": raw_params})
        return response.content
