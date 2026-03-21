from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class CreateBrandData:
    code: str
    name: str
    raw_parameters: Dict[str, Any]
    description: Optional[str] = None
    full_manual: Optional[str] = None
    logo_url: Optional[str] = None
    current_version: int = 1


@dataclass(frozen=True)
class UpdateBrandData:
    name: Optional[str] = None
    description: Optional[str] = None
    full_manual: Optional[str] = None
    logo_url: Optional[str] = None
    status: Optional[str] = None
    current_version: Optional[int] = None
