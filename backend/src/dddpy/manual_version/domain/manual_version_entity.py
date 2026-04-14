from datetime import datetime
from typing import Optional, Dict, Any


class ManualVersionEntity:
    def __init__(
        self,
        id: Optional[str],
        brand_id: str,
        version_number: int,
        full_content: str,
        raw_parameters: Dict[str, Any],
        status: str = "draft",
        url_pdf_manual: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.brand_id = brand_id
        self.version_number = version_number
        self.full_content = full_content
        self.raw_parameters = raw_parameters
        self.status = status
        self.url_pdf_manual = url_pdf_manual
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "brand_id": self.brand_id,
            "version_number": self.version_number,
            "full_content": self.full_content,
            "raw_parameters": self.raw_parameters,
            "status": self.status,
            "url_pdf_manual": self.url_pdf_manual,
            "created_at": self.serialize_date(self.created_at),
            "updated_at": self.serialize_date(self.updated_at),
        }

    @staticmethod
    def serialize_date(date_val: Any) -> Optional[str]:
        if not date_val:
            return None
        return date_val if isinstance(date_val, str) else date_val.isoformat()
