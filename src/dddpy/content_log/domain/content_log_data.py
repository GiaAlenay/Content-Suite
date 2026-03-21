from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class CreateContentLogData:
    brand_id: str
    creator_id: str
    content_data: str
    content_type: str
    agent_feedback: Optional[str] = None
    audit_by: Optional[str] = None
    status: Optional[str] = "PENDING"


@dataclass(frozen=True)
class UpdateContentLogData:
    agent_feedback: Optional[str] = None
    audit_by: Optional[str] = None
    status: Optional[str] = None
