from langchain_core.messages import SystemMessage

from pydantic import BaseModel, Field
from typing import List


class EditedSection(BaseModel):
    section_name: str = Field(description="Nombre de la sección editada.")
    content: str = Field(description="Contenido en Markdown de la sección.")
    order_number: int = Field(description="Posición de la sección.")


class EditorOutput(BaseModel):
    modified_sections: List[EditedSection] = Field(
        description="Lista de las secciones que fueron creadas o modificadas."
    )
    explanation_of_changes: str = Field(
        description="Breve resumen de qué se cambió para informar al usuario."
    )


class EditorAgent:
    def __init__(self, model):
        self.model = model.with_structured_output(EditorOutput)

    async def execute(
        self, brand_description: str, retrieved_context: str, refined_instruction: str
    ) -> EditorOutput:
        system_prompt = f"""
        Eres el Editor Senior de Manuales de Marca. 
        Tu tarea es aplicar cambios quirúrgicos al contenido existente.
        
        ADN DE LA MARCA (No debe violarse):
        {brand_description}
        
        CONTENIDO ACTUAL (Contexto para editar):
        {retrieved_context}
        
        INSTRUCCIÓN TÉCNICA:
        {refined_instruction}
        
        REGLAS:
        1. Mantén el formato Markdown profesional.
        2. Si la instrucción pide cambiar una sección específica, devuélvela editada.
        3. No inventes secciones que no se te pidieron, a menos que la instrucción lo indique.
        4. Asegúrate de que el tono sea coherente con el ADN.
        """

        return await self.model.ainvoke([SystemMessage(content=system_prompt)])
