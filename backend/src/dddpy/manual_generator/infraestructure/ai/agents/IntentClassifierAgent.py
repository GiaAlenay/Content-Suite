from langchain_core.prompts import ChatPromptTemplate
from typing import Literal
from pydantic import BaseModel, Field


class IntentClassification(BaseModel):
    intent: Literal["EDIT", "QA", "UNKNOWN"] = Field(
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
                    "Analiza el último mensaje del usuario. Determina si quiere EDITAR el manual (cambiar texto) o hacer una PREGUNTA (QA) sobre el contenido actual.",
                ),
                ("placeholder", "{messages}"),
            ]
        )

    async def execute(self, messages: list) -> IntentClassification:
        chain = self.prompt | self.llm
        return await chain.ainvoke({"messages": messages})
