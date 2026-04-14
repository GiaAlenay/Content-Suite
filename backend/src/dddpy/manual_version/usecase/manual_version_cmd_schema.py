from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class CreateManualVersionSchema(BaseModel):
    brand_id: str = Field(..., description="UUID de la marca")
    version_number: int = Field(..., gt=0, json_schema_extra={"example": 1})
    full_content: str = Field(..., description="Texto completo del manual")
    raw_parameters: Dict[str, Any] = Field(
        default={}, json_schema_extra={"example": {"tone": "profesional"}}
    )
    status: Optional[str] = "draft"
    url_pdf_manual: Optional[str] = None


class UpdateManualVersionSchema(BaseModel):
    status: Optional[str] = None
    url_pdf_manual: Optional[str] = None
    full_content: Optional[str] = None
    raw_parameters: Optional[Dict[str, Any]] = None
