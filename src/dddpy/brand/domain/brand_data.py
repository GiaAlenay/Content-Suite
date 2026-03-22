from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class CreateBrandData:
    name: str
    code: str
    description: Optional[str] = None
    logo_url: Optional[str] = None


@dataclass(frozen=True)
class UpdateBrandData:
    name: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    status: Optional[str] = None
