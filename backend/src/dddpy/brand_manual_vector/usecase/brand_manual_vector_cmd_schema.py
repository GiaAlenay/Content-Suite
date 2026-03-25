from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class CreateBrandManualVectorSchema(BaseModel):
    brand_id: str
    manual_record_id: str
    content_chunk: str
    embedding: List[float] = Field(..., min_items=768, max_items=768)
    creator_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class UpdateBrandManualVectorSchema(BaseModel):
    status: Optional[str] = Field(None, pattern="^(ACTIVE|INACTIVE)$")
    metadata: Optional[Dict[str, Any]] = None
