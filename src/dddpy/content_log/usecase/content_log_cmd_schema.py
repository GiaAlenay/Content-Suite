from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class CreateContentLogSchema(BaseModel):
    brand_id: str = Field(..., max_length=100)
    creator_id: str = Field(..., max_length=100)
    content_data: Optional[str] = Field(None, max_length=255)
    content_type: Optional[str] = Field(None)
    agent_feedback: Optional[str] = None
    audit_by: Optional[str] = Field(None)
    status: Optional[str] = Field(None, pattern="^(PENDING|)$")


class UpdateContentLogSchema(BaseModel):
    agent_feedback: Optional[str] = None
    audit_by: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(PENDING|)$")
