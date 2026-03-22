from pydantic import BaseModel, Field
from typing import Optional


class CreateBrandSchema(BaseModel):
    code: str = Field(..., max_length=50, example="QS-001")
    name: str = Field(..., max_length=100, example="Quinua-Snack")
    description: Optional[str] = Field(None, max_length=255)
    logo_url: Optional[str] = Field(None, example="https://storage.com/logo.png")


class UpdateBrandSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    logo_url: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(ACTIVE|INACTIVE)$")
