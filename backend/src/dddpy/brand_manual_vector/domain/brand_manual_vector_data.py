from dataclasses import dataclass
from typing import Optional, List, Dict, Any


@dataclass(frozen=True)
class CreateBrandManualVectorData:
    manual_version_id: str
    content_chunk: str
    embedding: List[float]
    manual_section_id: Optional[str] = None
    metadata: Dict[str, Any] = None
    status: str = "draft"


@dataclass(frozen=True)
class UpdateBrandManualVectorData:
    metadata: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
