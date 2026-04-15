from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field


class AuditReport(BaseModel):
    is_coherent: bool = Field(description="Si los inputs son coherentes con la marca")
    severity: str = Field(description="Nivel de conflicto: LOW, MEDIUM, HIGH")
    feedback: str = Field(description="Explicación detallada de las incoherencias")


class AuditAgent:
    def __init__(self, llm):
        self.llm = llm.with_structured_output(AuditReport)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "Eres un Auditor de Branding experto. Tu misión es detectar contradicciones entre la 'Descripción de Marca' y los 'Parámetros del Manual' que el usuario desea generar.",
                ),
                (
                    "user",
                    "DESCRIPCIÓN DE MARCA: {brand_desc}\n\nPARÁMETROS SOLICITADOS: {params}",
                ),
            ]
        )

    async def execute(self, brand_desc: str, params: dict) -> AuditReport:
        chain = self.prompt | self.llm
        return await chain.ainvoke({"brand_desc": brand_desc, "params": params})
