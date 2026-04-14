from dataclasses import dataclass
from typing import Optional


from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass(frozen=True)
class CreateChatHistoryData:
    session_id: str
    manual_version_id: str
    role: str
    content: str
    metadata: Dict[str, Any] = None
    order_number: int
