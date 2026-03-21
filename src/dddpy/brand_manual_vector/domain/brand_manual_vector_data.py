from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class CreateBrandManualVectorData:
    brand_id: str
    content_chunk: str
    embedding: str
    creator_id: str
    metadata: str


@dataclass(frozen=True)
class UpdateBrandManualVectorData:
    status: Optional[str] = None
