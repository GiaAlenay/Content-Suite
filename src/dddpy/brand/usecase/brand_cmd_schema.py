from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class CreateBrandSchema(BaseModel):
    code: str = Field(..., max_length=50, example="QS-001")
    name: str = Field(..., max_length=100, example="Quinua-Snack")
    description: Optional[str] = Field(None, max_length=255)
    raw_parameters: Dict[str, Any] = Field(
        ...,
        example={"tone": "Divertido", "target": "Gen Z", "product": "Snack de quinua"},
    )
    full_manual: Optional[str] = Field(None)
    logo_url: Optional[str] = Field(None)
    current_version: Optional[int] = Field(1)


class UpdateBrandSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    full_manual: Optional[str] = None
    logo_url: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(ACTIVE|INACTIVE)$")
    current_version: Optional[int] = None
