from enum import Enum
from pydantic import BaseModel, Field
from typing import List, Optional


class ManualRequestSchema(BaseModel):
    target_audience: str = Field(..., example="Emprendedores jóvenes de 18-30 años")
    core_values: List[str] = Field(
        ..., example=["Innovación", "Transparencia", "Sostenibilidad"]
    )
    tone_preference: str = Field(..., example="Cercano y motivador")
    forbidden_topics: List[str] = Field(
        default_factory=list, example=["Política", "Religión"]
    )
    additional_notes: Optional[str] = Field(
        None,
        description="Instrucciones libres del usuario",
        example="Incluye una sección específica para atención al cliente en Twitter",
    )
    brand_colors: List[str] = Field(
        ...,
        example=["Azul Cobalto #0047AB", "Blanco Puro #FFFFFF"],
        description="Colores principales de la marca",
    )
    visual_style: str = Field(
        ...,
        example="Minimalista, con mucho espacio en blanco y fotografía lifestyle",
        description="Estilo visual general",
    )
    logo_guidelines: Optional[str] = Field(
        "El logo debe tener un área de protección igual a su altura. No usar sobre fondos complejos.",
        description="Reglas básicas de uso del logo",
    )


class AuditManualSchema(BaseModel):
    is_coherent: bool = Field(
        description="Indica si los parámetros no se contradicen con la marca"
    )
    severity: str = Field(description="LOW (sugerencia) o HIGH (bloqueante)")
    feedback: List[str] = Field(description="Lista de conflictos encontrados")
    suggestions: str = Field(description="Cómo mejorar los inputs para un mejor manual")


class RefinementRequest(BaseModel):
    refinement_prompt: str


class VectorMetadataSchema(BaseModel):
    section_name: str = Field(
        ..., description="Nombre de la sección (ej. Identidad Visual)"
    )
    chunk_index: int = Field(..., description="Orden secuencial del fragmento")
    is_header: bool = Field(
        default=False, description="Indica si el texto es un título"
    )
    content_type: str = Field(
        default="text", description="Tipo de contenido: text, list, table"
    )
    page_number: Optional[int] = Field(None, description="Número de página de origen")
    token_count: Optional[int] = Field(
        None, description="Cantidad de tokens en este chunk"
    )

    class Config:
        extra = "allow"


class ChatMessageMetadataSchema(BaseModel):
    source_nodes: List[str] = Field(
        default_factory=list,
        description="Lista de UUIDs de la tabla brand_manuals_vectors usados como contexto",
    )
    model_used: str = Field(
        ..., example="gpt-4o", description="Modelo de LLM que generó la respuesta"
    )
    total_tokens: int = Field(
        ..., description="Costo total de la interacción (prompt + completion)"
    )
    retrieval_score: Optional[float] = Field(
        None, description="Puntaje promedio de relevancia de los fragmentos recuperados"
    )
    audit_status: str = Field(
        default="PENDING",
        description="Resultado del Agente Auditor (PASSED, FAILED, WARNING)",
    )
    audit_feedback: Optional[List[str]] = Field(
        None, description="Comentarios del auditor"
    )

    class Config:
        extra = "allow"


class ActionType(str, Enum):
    NAVIGATE = "navigate"
    EDIT = "edit"
    QUERY = "query"
    EXPORT = "export"  # Para descargar el manual
    TALK = "talk"  # Saludos o charla casual
    UNKNOWN = "unknown"  # Fuera de scope


class IntentSchema(BaseModel):
    action: ActionType
    target_version_logic: Optional[str] = Field(
        None, description="Lógica de destino: 'FIRST', 'PREVIOUS', 'SPECIFIC', 'LAST'"
    )
    specific_version_number: Optional[int] = Field(None)
    editing_instruction: Optional[str] = Field(
        None, description="Lo que el usuario quiere cambiar"
    )


def handle_action(intent: IntentSchema):
    match intent.action:
        case ActionType.NAVIGATE:
            return repo_version.move_to(intent.target_version)
        case ActionType.EDIT:
            return service_editor.apply_change(intent.editing_instruction)
        case ActionType.QUERY:
            return service_rag.ask(intent.query)
        case ActionType.TALK:
            return llm.simple_chat("Responde amablemente como asistente de marca")
        case _:
            return "Lo siento, mi enfoque es la gestión de tu marca. ¿En qué sección del manual trabajamos hoy?"
