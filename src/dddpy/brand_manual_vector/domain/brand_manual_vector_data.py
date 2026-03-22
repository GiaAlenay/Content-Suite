from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass(frozen=True)
class CreateBrandManualVectorData:
    brand_id: str
    manual_record_id: str
    content_chunk: str
    embedding: List[float]
    creator_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class UpdateBrandManualVectorData:
    status: Optional[str] = None
