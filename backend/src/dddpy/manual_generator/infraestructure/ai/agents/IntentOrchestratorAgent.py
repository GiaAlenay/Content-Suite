from langchain_core.messages import SystemMessage, BaseMessage

from pydantic import BaseModel, Field
from typing import List, Literal, Optional


class TaskSchema(BaseModel):
    task_type: Literal["EDIT", "QA", "CLARIFY", "OUT_OF_SCOPE", "APPROVE"] = Field(
        description="El tipo de acción a realizar."
    )
    description: str = Field(
        description="Breve explicación de por qué se eligió esta tarea."
    )
    target_sections: Optional[List[str]] = Field(
        default=None,
        description="Nombres o IDs de las secciones involucradas si es un EDIT o QA específico.",
    )


class OrchestratorOutput(BaseModel):
    tasks: List[TaskSchema] = Field(
        description="Lista de tareas identificadas en el prompt."
    )
    reasoning: str = Field(description="Análisis global de la petición del usuario.")


class IntentOrchestratorAgent:
    def __init__(self, model):
        # Forzamos al modelo a responder con nuestro esquema
        self.model = model.with_structured_output(OrchestratorOutput)

    async def execute(
        self, history: List[BaseMessage], brand_description: str
    ) -> OrchestratorOutput:
        system_prompt = f"""
        Eres el Orquestador de un sistema de creación de Manuales de Marca. 
        Tu objetivo es analizar la petición del usuario y desglosarla en tareas técnicas.
        
        CONTEXTO DE MARCA: {brand_description}
        
        REGLAS DE CLASIFICACIÓN:
        1. EDIT: El usuario pide cambiar, agregar o eliminar algo del manual.
        2. QA: El usuario hace una pregunta sobre el contenido existente del manual.
        3. CLARIFY: La petición es ambigua (ej: "cambia eso") o le falta información.
        4. OUT_OF_SCOPE: Peticiones que no tienen que ver con el manual (ej: "cuéntame un chiste").
        5. APPROVE: El usuario manifiesta explícitamente que el manual está listo para publicarse.
        
        Si hay múltiples intenciones, inclúyelas todas en la lista de tareas.
        """

        # Combinamos el sistema con el historial de la sesión
        messages = [SystemMessage(content=system_prompt)] + history
        return await self.model.ainvoke(messages)


# from langchain_core.prompts import ChatPromptTemplate
# from typing import Literal
# from pydantic import BaseModel, Field


# class IntentClassification(BaseModel):
#     intent: Literal["EDIT", "QA", "RESTORE", "UNKNOWN"] = Field(
#         description="La intención detectada"
#     )
#     reasoning: str = Field(description="Por qué se clasificó así")


# class IntentClassifierAgent:
#     def __init__(self, llm):
#         self.llm = llm.with_structured_output(IntentClassification)
#         self.prompt = ChatPromptTemplate.from_messages(
#             [
#                 (
#                     "system",
#                     """Analiza el último mensaje del usuario para determinar su intención:
#             - EDIT: El usuario quiere modificar, agregar o eliminar contenido del manual actual.
#             - QA: El usuario tiene dudas o quiere consultar información del manual.
#             - RESTORE: El usuario quiere volver a una versión anterior, deshacer cambios o recuperar el estado previo.
#             - UNKNOWN: No se identifica ninguna de las anteriores.""",
#                 ),
#                 ("placeholder", "{messages}"),
#             ]
#         )

#     async def execute(self, messages: list) -> IntentClassification:
#         chain = self.prompt | self.llm
#         return await chain.ainvoke({"messages": messages})
