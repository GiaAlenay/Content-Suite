from datetime import datetime
from typing import Optional, Dict, Any


class BrandEntity:
    def __init__(
        self,
        id: Optional[str],
        name: str,
        code: str,
        description: Optional[str] = None,
        logo_url: Optional[str] = None,
        status: str = "ACTIVE",
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.name = name
        self.code = code
        self.description = description
        self.logo_url = logo_url
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "logo_url": self.logo_url,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
