from pydantic import BaseModel, Field
from typing import List
from langchain_core.messages import SystemMessage


class RetrievalStrategy(BaseModel):
    search_queries: List[str] = Field(
        description="Frases para buscar en la DB de vectores."
    )
    requires_full_manual: bool = Field(
        description="¿El cambio es global y requiere todo el manual?"
    )
    reasoning: str = Field(description="Por qué se eligió esta estrategia.")


class ContextDiscoveryAgent:
    def __init__(self, model):
        self.model = model.with_structured_output(RetrievalStrategy)

    async def execute(
        self, user_prompt: str, planned_tasks: List[dict]
    ) -> RetrievalStrategy:
        system_prompt = f"""
        Eres el Estratega de Contexto. Tu misión es determinar qué información del manual 
        necesitamos recuperar para cumplir con la petición del usuario.
        
        PETICIÓN: "{user_prompt}"
        TAREAS: {planned_tasks}
        
        Si el usuario pide un cambio específico (ej: 'cambia el logo'), genera queries de búsqueda.
        Si pide algo general (ej: 'haz que todo suene más juvenil'), marca requires_full_manual como true.
        """
        return await self.model.ainvoke([SystemMessage(content=system_prompt)])
