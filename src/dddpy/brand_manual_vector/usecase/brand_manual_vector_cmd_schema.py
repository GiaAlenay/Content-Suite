from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class CreateBrandManualVectorSchema(BaseModel):
    brand_id: str = Field(..., max_length=100)
    content_chunk: str = Field(..., max_length=255)
    embedding: str = Field(...)
    creator_id: str = Field(...)
    metadata: str = Field(...)


class UpdateBrandManualVectorSchema(BaseModel):
    status: Optional[str] = Field(None, pattern="^(ACTIVE|INACTIVE)$")
