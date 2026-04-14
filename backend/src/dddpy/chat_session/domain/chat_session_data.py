from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CreateChatSessionData:
    brand_id: str
    current_version_id: str
    user_id: Optional[str] = None


@dataclass(frozen=True)
class UpdateChatSessionData:
    current_version_id: str
