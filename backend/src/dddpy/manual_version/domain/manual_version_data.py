from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class CreateManualVersionData:
    brand_id: str
    version_number: int
    full_content: str
    raw_parameters: Dict[str, Any]
    status: str = "draft"
    url_pdf_manual: Optional[str] = None


@dataclass(frozen=True)
class UpdateManualVersionData:
    status: Optional[str] = None
    url_pdf_manual: Optional[str] = None
    full_content: Optional[str] = None
    raw_parameters: Optional[Dict[str, Any]] = None
