from datetime import datetime
from typing import Optional, Dict, Any


class ChatHistoryEntity:
    def __init__(
        self,
        id: Optional[str],
        session_id: str,
        manual_version_id: str,
        role: str,
        content: str,
        order_number: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.session_id = session_id
        self.manual_version_id = manual_version_id
        self.role = role
        self.content = content
        self.order_number = order_number
        self.metadata = metadata or {}
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "session_id": self.session_id,
            "manual_version_id": self.manual_version_id,
            "role": self.role,
            "content": self.content,
            "order_number": self.order_number,
            "metadata": self.metadata,
            "created_at": self.serialize_date(self.created_at),
            "updated_at": self.serialize_date(self.updated_at),
        }

    @staticmethod
    def serialize_date(date_val: Any) -> Optional[str]:
        if not date_val:
            return None
        return date_val if isinstance(date_val, str) else date_val.isoformat()
