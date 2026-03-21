from pydantic import BaseModel, Field
from typing import Optional


class CreateBrandSchema(BaseModel):
    code: str = Field(..., max_length=50)
    name: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    full_manual: str = Field(...)


class UpdateBrandSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=255)
    full_manual: Optional[str] = Field(None)
