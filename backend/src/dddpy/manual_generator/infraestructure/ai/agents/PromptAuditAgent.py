from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from typing import Optional
from pydantic import BaseModel, Field


class ChatAuditOutput(BaseModel):
    is_coherent: bool = Field(
        description="Indica si la petición del usuario es coherente con el ADN de la marca."
    )
    reasoning: str = Field(
        description="Explicación técnica de por qué se acepta o rechaza el cambio."
    )
    suggested_refusal_message: Optional[str] = Field(
        description="Mensaje amable para el usuario si la petición es rechazada."
    )
    severity_score: int = Field(
        ge=1,
        le=5,
        description="Nivel de conflicto: 1 (mínimo) a 5 (ruptura total de marca).",
    )


class PromptAuditAgent:
    def __init__(self, model):
        self.model = model.with_structured_output(ChatAuditOutput)

    async def execute(
        self, brand_description: str, user_prompt: str
    ) -> ChatAuditOutput:
        system_prompt = f"""
        Eres el Guardián de Marca (Brand Guardian).
        Tu misión es proteger la integridad de la marca descrita abajo.
        
        ADN DE LA MARCA:
        {brand_description}
        
        REGLA DE ORO:
        Si el usuario pide un cambio que contradice los valores, el tono o la estética 
        definida en el ADN (ej: pedir algo 'informal' cuando la marca es 'corporativa de lujo'),
        debes marcar 'is_coherent: false'.
        
        PETICIÓN DEL USUARIO:
        "{user_prompt}"
        """

        # Enviamos solo la instrucción actual y el ADN para un juicio limpio
        messages = [SystemMessage(content=system_prompt)]
        return await self.model.ainvoke(messages)
