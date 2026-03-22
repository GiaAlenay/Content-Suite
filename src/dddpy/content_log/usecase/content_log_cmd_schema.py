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
    agent_feedback: Optional[str] = None
    audit_by: Optional[str] = None


class UpdateContentLogSchema(BaseModel):
    status: Optional[str] = Field(None, pattern="^(PENDING|APPROVED|REJECTED)$")
    agent_feedback: Optional[str] = None
    audit_by: Optional[str] = None
