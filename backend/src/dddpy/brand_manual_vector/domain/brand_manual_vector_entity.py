from datetime import datetime
from typing import Optional, List, Dict, Any


class BrandManualVectorEntity:
    def __init__(
        self,
        id: Optional[str],
        manual_version_id: str,
        content_chunk: str,
        embedding: List[float],
        manual_section_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        status: str = "draft",
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        self.id = id
        self.manual_version_id = manual_version_id
        self.manual_section_id = manual_section_id
        self.content_chunk = content_chunk
        self.embedding = embedding
        self.metadata = metadata or {}
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "manual_version_id": self.manual_version_id,
            "manual_section_id": self.manual_section_id,
            "content_chunk": self.content_chunk,
            "embedding": self.embedding,
            "metadata": self.metadata,
            "status": self.status,
            "created_at": self.serialize_date(self.created_at),
            "updated_at": self.serialize_date(self.updated_at),
        }

    @staticmethod
    def serialize_date(date_val: Any) -> Optional[str]:
        if not date_val:
            return None
        return date_val if isinstance(date_val, str) else date_val.isoformat()


class BrandManualVectorSimilarityEntity:
    def __init__(self, id: Optional[str], content_chunk: str, similarity: int) -> None:
        self.id = id
        self.similarity = similarity
        self.content_chunk = content_chunk

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "similarity": self.similarity,
            "content_chunk": self.content_chunk,
        }
