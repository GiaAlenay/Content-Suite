from datetime import datetime
from typing import Optional, Dict, Any


class ManualRecordEntity:
    def __init__(
        self,
        id: Optional[str],
        brand_id: str,
        version: int,
        full_manual: str,
        raw_parameters: Dict[str, Any],
        is_current_version: bool = False,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.brand_id = brand_id
        self.version = version
        self.full_manual = full_manual
        self.raw_parameters = raw_parameters
        self.is_current_version = is_current_version
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "brand_id": self.brand_id,
            "version": self.version,
            "full_manual": self.full_manual,
            "raw_parameters": self.raw_parameters,
            "is_current_version": self.is_current_version,
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
