from typing import Annotated, List, Optional, TypedDict
from operator import add
from langchain_core.messages import BaseMessage


class ManualState1(TypedDict):
    brand_id: str
    brand_name: str
    brand_description: str
    manual_version_id: Optional[str]
    chat_session_id: Optional[str]
    raw_params: dict

    audit_report: Optional[dict]
    full_content: Optional[str]
    sections: List[dict]

    messages: Annotated[List[BaseMessage], add]

    next_step: str


class ManualState(TypedDict):
    # IDs de rastreo y contexto base
    brand_id: str
    brand_name: str
    brand_description: str
    manual_version_id: Optional[str]
    chat_session_id: Optional[str]

    # Datos de entrada
    raw_params: dict  # Parámetros iniciales del Punto 1
    messages: Annotated[List[BaseMessage], add]  # Historial (User, AI, System)

    # Planificación y Auditoría de Chat
    planned_tasks: List[dict]  # Lista de intenciones desglosadas por el Orchestrator
    current_task_idx: int  # Para iterar sobre intenciones múltiples
    chat_audit_report: Optional[dict]  # Auditoría específica del prompt del chat

    # Manejo de contenido dinámico (Granularidad)
    retrieved_context: Optional[
        str
    ]  # Fragmentos del manual recuperados para editar/consultar
    refined_prompt: Optional[str]  # El "comando" técnico generado por el Upgrader
    full_content: Optional[str]  # Contenido completo de la versión actual
    sections: List[dict]  # Secciones individuales de la versión actual

    # Control de flujo
    next_step: str
