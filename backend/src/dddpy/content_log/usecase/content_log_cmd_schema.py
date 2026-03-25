from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class CreateContentLogSchema(BaseModel):
    brand_id: str
    creator_id: str
    content_data: Dict[str, Any] = Field(
        ..., example={"text": "Hola mundo", "image_url": "..."}
    )
    content_type: str = Field(..., example="INSTAGRAM_POST")
    status: Optional[str] = Field(None, pattern="^(PENDING|APPROVED|REJECTED)$")
    prompt_origin: Optional[str] = Field(None, example="Quiero un post")
    agent_feedback: Optional[str] = None
    audit_by: Optional[str] = None


class UpdateContentLogSchema(BaseModel):
    status: Optional[str] = Field(None, pattern="^(APPROVED|REJECTED)$")
    agent_feedback: Optional[str] = None
    audit_by: Optional[str] = None


class GenerateContentRequest(BaseModel):
    user_prompt: str = Field(..., example="Crea un post para instagram...")
    content_type: str = Field(..., example="INSTAGRAM_POST")


class AuditResponseSchema(BaseModel):
    suggested_status: str = Field(description="Debe ser 'APPROVED' o 'REJECTED'")
    score: int = Field(description="Puntaje de cumplimiento de 1 a 10")
    feedback: str = Field(description="Explicación detallada de la auditoría")
