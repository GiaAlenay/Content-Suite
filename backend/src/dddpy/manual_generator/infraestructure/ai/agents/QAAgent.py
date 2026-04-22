from pydantic import BaseModel, Field
from typing import List, Optional
from langchain_core.messages import SystemMessage, HumanMessage


class QAOutput(BaseModel):
    answer: str = Field(description="La respuesta directa a la pregunta del usuario.")
    sources: List[str] = Field(
        description="Nombres de las secciones del manual utilizadas para responder."
    )
    confidence_score: float = Field(
        description="Nivel de seguridad de la respuesta (0.0 a 1.0)."
    )
    suggested_follow_up: Optional[str] = Field(
        description="Una pregunta sugerida para profundizar en el tema."
    )


class QAAgent:
    def __init__(self, model):
        self.model = model.with_structured_output(QAOutput)

    async def execute(self, user_question: str, retrieved_context: str) -> QAOutput:
        system_prompt = f"""
        Eres el Asistente Experto del Manual de Marca. 
        Tu objetivo es responder preguntas basadas UNICAMENTE en el contenido del manual proporcionado.
        
        CONTENIDO DEL MANUAL RECUPERADO:
        {retrieved_context}
        
        REGLAS:
        1. Si la respuesta no está en el contenido, di honestamente que no cuentas con esa información.
        2. Sé preciso y mantén el tono de la marca.
        3. Cita las secciones de donde sacaste la información.
        """

        # Invocamos al modelo con la pregunta y el contexto
        return await self.model.ainvoke(
            [SystemMessage(content=system_prompt), HumanMessage(content=user_question)]
        )
