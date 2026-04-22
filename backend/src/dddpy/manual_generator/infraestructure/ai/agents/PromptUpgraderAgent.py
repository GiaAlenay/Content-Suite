from pydantic import BaseModel, Field
from langchain_core.messages import SystemMessage


class RefinedInstruction(BaseModel):
    technical_instruction: str = Field(
        description="La instrucción refinada y técnica para el Editor."
    )
    edit_scope: str = Field(
        description="Resumen de qué partes específicas se verán afectadas (ej: 'Solo sección 2' o 'Global')."
    )
    tone_guidelines: str = Field(
        description="Recordatorio del tono que se debe mantener basado en el ADN de marca."
    )


class PromptUpgraderAgent:
    def __init__(self, model):
        self.model = model.with_structured_output(RefinedInstruction)

    async def execute(
        self, user_prompt: str, brand_description: str, retrieved_context: str
    ) -> RefinedInstruction:
        system_prompt = f"""
        Eres un Ingeniero de Prompts experto en Branding. 
        Tu misión es redactar una instrucción técnica para un Editor de contenido.
        
        ADN DE LA MARCA:
        {brand_description}
        
        CONTEXTO RECUPERADO DEL MANUAL (Fragmentos relevantes):
        {retrieved_context}
        
        INSTRUCCIÓN:
        1. Analiza lo que el usuario pidió: "{user_prompt}"
        2. Genera una 'technical_instruction' que sea imperativa y precisa. 
        3. Asegúrate de que la instrucción mencione explícitamente qué partes del 
           'CONTEXTO RECUPERADO' debe modificar y qué debe dejar intacto.
        """

        return await self.model.ainvoke([SystemMessage(content=system_prompt)])
