from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class ContentLogEntity:
    id: Optional[str]
    brand_id: str
    creator_id: str
    content_data: Optional[str] = None
    content_type: Optional[str] = None
    audit_by: Optional[str] = None
    agent_feedback: Optional[str] = None
    status: str = "PENDING"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convierte la entidad a un diccionario para respuestas de API o logs."""
        return {
            "id": self.id,
            "brand_id": self.brand_id,
            "creator_id": self.creator_id,
            "content_data": self.content_data,
            "content_type": self.content_type,
            "audit_by": self.audit_by,
            "agent_feedback": self.agent_feedback,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
