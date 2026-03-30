from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


class CreateContentLogSchema(BaseModel):
    brand_id: str
    creator_id: str
    content_data: Dict[str, Any] = Field(
        ..., example={"text": "Hola mundo", "image_url": "..."}
    )
    content_type: str = Field(..., example="INSTAGRAM_POST")
    status: Optional[str] = Field(None, pattern="^(PENDING|APPROVED|REJECTED|CREATED)$")
    prompt_origin: Optional[str] = Field(None, example="Quiero un post")
    agent_feedback: Optional[str] = Field(None)
    audit_by: Optional[str] = Field(None)
    parent_id: Optional[str] = Field(None)


class UpdateContentLogSchema(BaseModel):
    status: Optional[str] = Field(None, pattern="^(PENDING|APPROVED|REJECTED)$")
    agent_feedback: Optional[str] = Field(None)
    audit_by: Optional[str] = Field(None)


class GenerateContentRequest(BaseModel):
    user_prompt: str = Field(..., example="Crea un post para instagram...")
    content_type: str = Field(..., example="INSTAGRAM_POST")
    parent_log_id: Optional[str] = Field(None)


class AuditResponseSchema(BaseModel):
    suggested_status: str = Field(description="Debe ser 'APPROVED' o 'REJECTED'")
    score: int = Field(description="Puntaje de cumplimiento de 1 a 10")
    feedback: str = Field(description="Explicación detallada de la auditoría")


class AuditPromptSchema(BaseModel):
    is_allowed: bool = Field(
        description="¿El prompt es seguro y coherente para generar?"
    )
    is_type_match: bool = Field(
        description="¿El texto del prompt coincide con el target_content seleccionado?"
    )
    detected_content_type: str = Field(
        description="El tipo de contenido que la IA detecta en el texto"
    )
    severity: str = Field(description="LOW o HIGH")
    feedback: List[str] = Field(description="Explicación de conflictos o sugerencias")
    improved_prompt: str = Field(
        description="Versión optimizada del prompt para el motor de generación"
    )
