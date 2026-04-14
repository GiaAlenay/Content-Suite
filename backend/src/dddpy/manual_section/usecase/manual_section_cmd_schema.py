from pydantic import BaseModel, Field
from typing import Dict, Any, Optional


class CreateManualSectionSchema(BaseModel):
    manual_version_id: str = Field(..., description="UUID de la versión del manual")
    section_name: str = Field(
        ..., description="Nombre de la sección (ej. Introducción)"
    )
    content: str = Field(..., description="Contenido de la sección")
    order_number: int = Field(..., ge=0, json_schema_extra={"example": 1})
