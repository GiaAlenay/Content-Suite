from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class BrandManualVectorEntity:
    id: Optional[str]
    brand_id: str
    content_chunk: Optional[str] = None
    embedding: Optional[str] = None
    metadata: Optional[str] = None
    creator_id: Optional[str] = None
    status: str = "ACTIVE"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convierte la entidad a un diccionario para respuestas de API o logs."""
        return {
            "id": self.id,
            "brand_id": self.brand_id,
            "content_chunk": self.content_chunk,
            "embedding": self.embedding,
            "creator_id": self.creator_id,
            "status": self.status,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
