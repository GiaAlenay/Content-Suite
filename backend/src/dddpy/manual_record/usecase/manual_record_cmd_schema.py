from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class CreateManualRecordSchema(BaseModel):
    brand_id: str = Field(..., description="UUID de la marca")
    version: int = Field(..., gt=0, example=1)
    full_manual: str = Field(..., description="Texto completo del manual generado")
    raw_parameters: Dict[str, Any] = Field(
        ..., example={"tone": "profesional", "target": "corporativo"}
    )
    is_current_version: Optional[bool] = True
    url_manual: Optional[str] = None
    agent_feedback: Optional[Dict[str, Any]] = None


class UpdateManualRecordSchema(BaseModel):
    is_current_version: Optional[bool] = None
    url_manual: Optional[str] = None
    agent_feedback: Optional[Dict[str, Any]] = None
