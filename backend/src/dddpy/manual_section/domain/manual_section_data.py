from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CreateManualSectionData:
    manual_version_id: str
    section_name: str
    content: str
    order_number: int


@dataclass(frozen=True)
class UpdateManualSectionData:
    section_name: Optional[str] = None
    content: Optional[str] = None
    order_number: Optional[int] = None
