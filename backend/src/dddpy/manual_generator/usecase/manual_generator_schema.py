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
    brand_colors: List[str] = Field(
        ...,
        example=["Azul Cobalto #0047AB", "Blanco Puro #FFFFFF"],
        description="Colores principales de la marca",
    )
    visual_style: str = Field(
        ...,
        example="Minimalista, con mucho espacio en blanco y fotografía lifestyle",
        description="Estilo visual general",
    )
    logo_guidelines: Optional[str] = Field(
        "El logo debe tener un área de protección igual a su altura. No usar sobre fondos complejos.",
        description="Reglas básicas de uso del logo",
    )


class AuditManualSchema(BaseModel):
    is_coherent: bool = Field(
        description="Indica si los parámetros no se contradicen con la marca"
    )
    severity: str = Field(description="LOW (sugerencia) o HIGH (bloqueante)")
    feedback: List[str] = Field(description="Lista de conflictos encontrados")
    suggestions: str = Field(description="Cómo mejorar los inputs para un mejor manual")
