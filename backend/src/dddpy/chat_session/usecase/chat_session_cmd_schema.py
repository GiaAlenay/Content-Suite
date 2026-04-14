from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class CreateChatSessionSchema(BaseModel):
    brand_id: str = Field(..., description="UUID de la marca vinculada al chat")
    current_version_id: str = Field(
        ..., description="UUID de la versión del manual a consultar"
    )
    user_id: Optional[str] = Field(None, description="UUID del usuario (opcional)")


class UpdateChatSessionSchema(BaseModel):
    current_version_id: str = Field(
        ..., description="Nueva versión del manual para esta sesión"
    )
