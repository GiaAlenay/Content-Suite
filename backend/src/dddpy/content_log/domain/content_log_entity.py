from datetime import datetime
from typing import Optional, Dict, Any


class ContentLogEntity:
    def __init__(
        self,
        id: Optional[str],
        brand_id: str,
        creator_id: str,
        content_data: Dict[str, Any],
        content_type: str,
        status: str = "PENDING",
        agent_feedback: Optional[str] = None,
        audit_by: Optional[str] = None,
        prompt_origin: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.brand_id = brand_id
        self.creator_id = creator_id
        self.content_data = content_data
        self.content_type = content_type
        self.status = status
        self.agent_feedback = agent_feedback
        self.audit_by = audit_by
        self.prompt_origin = prompt_origin
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "brand_id": self.brand_id,
            "creator_id": self.creator_id,
            "content_data": self.content_data,
            "content_type": self.content_type,
            "status": self.status,
            "agent_feedback": self.agent_feedback,
            "audit_by": self.audit_by,
            "prompt_origin": self.prompt_origin,
            "created_at": (
                self.created_at
                if isinstance(self.created_at, str)
                else (self.created_at.isoformat() if self.created_at else None)
            ),
            "updated_at": (
                self.updated_at
                if isinstance(self.updated_at, str)
                else (self.updated_at.isoformat() if self.updated_at else None)
            ),
        }
