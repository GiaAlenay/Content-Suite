from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CreateBrandData:
    code: str
    name: str
    full_manual: str
    description: Optional[str] = None


@dataclass(frozen=True)
class UpdateBrandData:
    name: Optional[str] = None
    description: Optional[str] = None
    full_manual: Optional[str] = None
