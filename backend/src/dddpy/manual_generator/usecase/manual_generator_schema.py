from pydantic import BaseModel, Field
from typing import List, Optional


class ManualRequestSchema(BaseModel):
    target_audience: str = Field(..., example="Emprendedores jóvenes de 18-30 años")
    core_values: List[str] = Field(
        ..., example=["Innovación", "Transparencia", "Sostenibilidad"]
    )
    tone_preference: str = Field(..., example="Cercano y motivador")
    forbidden_topics: List[str] = Field(
        default_factory=list, example=["Política", "Religión"]
    )
    additional_notes: Optional[str] = Field(
        None,
        description="Instrucciones libres del usuario",
        example="Incluye una sección específica para atención al cliente en Twitter",
    )
