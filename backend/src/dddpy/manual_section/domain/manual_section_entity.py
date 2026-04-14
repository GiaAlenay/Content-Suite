from datetime import datetime
from typing import Optional, Dict, Any


class ManualSectionEntity:
    def __init__(
        self,
        id: Optional[str],
        manual_version_id: str,
        section_name: str,
        content: str,
        order_number: int,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.manual_version_id = manual_version_id
        self.section_name = section_name
        self.content = content
        self.order_number = order_number
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "manual_version_id": self.manual_version_id,
            "section_name": self.section_name,
            "content": self.content,
            "order_number": self.order_number,
            "created_at": self.serialize_date(self.created_at),
            "updated_at": self.serialize_date(self.updated_at),
        }

    @staticmethod
    def serialize_date(date_val: Any) -> Optional[str]:
        if not date_val:
            return None
        return date_val if isinstance(date_val, str) else date_val.isoformat()
