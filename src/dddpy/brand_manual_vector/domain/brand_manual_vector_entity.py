from datetime import datetime
from typing import Optional, List, Dict, Any


class BrandManualVectorEntity:
    def __init__(
        self,
        id: Optional[str],
        brand_id: str,
        manual_record_id: str,
        content_chunk: str,
        embedding: List[float],
        creator_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        status: str = "ACTIVE",
        created_at: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.brand_id = brand_id
        self.manual_record_id = manual_record_id
        self.content_chunk = content_chunk
        self.embedding = embedding
        self.creator_id = creator_id
        self.metadata = metadata
        self.status = status
        self.created_at = created_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "brand_id": self.brand_id,
            "manual_record_id": self.manual_record_id,
            "content_chunk": self.content_chunk,
            "embedding": self.embedding,
            "creator_id": self.creator_id,
            "metadata": self.metadata,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
