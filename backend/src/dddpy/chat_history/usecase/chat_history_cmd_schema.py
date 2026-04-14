from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class CreateChatHistorySchema(BaseModel):
    session_id: str = Field(..., description="UUID de la sesión de chat")
    manual_version_id: str = Field(
        ..., description="Versión del manual usada para este mensaje"
    )
    role: str = Field(..., description="Rol del emisor: user, assistant o system")
    content: str = Field(..., description="Contenido del mensaje")
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        json_schema_extra={"example": {"reasoning": "El usuario preguntó sobre X..."}},
    )
    order_number: int = Field(..., ge=1, json_schema_extra={"example": 1})
