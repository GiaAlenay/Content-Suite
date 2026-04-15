from langchain_core.prompts import ChatPromptTemplate
from typing import Literal
from pydantic import BaseModel, Field


class IntentClassification(BaseModel):
    intent: Literal["EDIT", "QA", "RESTORE", "UNKNOWN"] = Field(
        description="La intención detectada"
    )
    reasoning: str = Field(description="Por qué se clasificó así")


class IntentClassifierAgent:
    def __init__(self, llm):
        self.llm = llm.with_structured_output(IntentClassification)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Analiza el último mensaje del usuario para determinar su intención:
            - EDIT: El usuario quiere modificar, agregar o eliminar contenido del manual actual.
            - QA: El usuario tiene dudas o quiere consultar información del manual.
            - RESTORE: El usuario quiere volver a una versión anterior, deshacer cambios o recuperar el estado previo.
            - UNKNOWN: No se identifica ninguna de las anteriores.""",
                ),
                ("placeholder", "{messages}"),
            ]
        )

    async def execute(self, messages: list) -> IntentClassification:
        chain = self.prompt | self.llm
        return await chain.ainvoke({"messages": messages})
