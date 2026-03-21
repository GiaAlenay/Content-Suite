from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class BrandEntity:
    id: Optional[str]
    code: str
    name: str
    raw_parameters: Dict[str, Any]
    description: Optional[str] = None
    full_manual: Optional[str] = None
    current_version: int = 1
    logo_url: Optional[str] = None
    status: str = "ACTIVE"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convierte la entidad a un diccionario para respuestas de API o logs."""
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "description": self.description,
            "full_manual": self.full_manual,
            "current_version": self.current_version,
            "logo_url": self.logo_url,
            "raw_parameters": self.raw_parameters,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
