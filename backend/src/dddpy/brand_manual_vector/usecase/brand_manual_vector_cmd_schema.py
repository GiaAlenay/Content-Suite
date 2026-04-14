from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class CreateBrandManualVectorSchema(BaseModel):
    manual_version_id: str = Field(..., description="UUID de la versión del manual")
    content_chunk: str = Field(..., description="Fragmento de texto para el embedding")
    embedding: List[float] = Field(..., min_items=768, max_items=768)
    manual_section_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    status: Optional[str] = "draft"


class UpdateBrandManualVectorSchema(BaseModel):
    metadata: Optional[Dict[str, Any]] = None
    status: Optional[str] = Field(None, pattern="^(draft|pending)$")
