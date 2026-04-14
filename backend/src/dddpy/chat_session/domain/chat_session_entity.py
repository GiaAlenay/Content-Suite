from datetime import datetime
from typing import Optional, Dict, Any


class ChatSessionEntity:
    def __init__(
        self,
        id: Optional[str],
        brand_id: str,
        current_version_id: str,
        user_id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.user_id = user_id
        self.brand_id = brand_id
        self.current_version_id = current_version_id
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "brand_id": self.brand_id,
            "current_version_id": self.current_version_id,
            "created_at": self.serialize_date(self.created_at),
            "updated_at": self.serialize_date(self.updated_at),
        }

    @staticmethod
    def serialize_date(date_val: Any) -> Optional[str]:
        if not date_val:
            return None
        return date_val if isinstance(date_val, str) else date_val.isoformat()
