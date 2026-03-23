from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class CreateContentLogData:
    brand_id: str
    creator_id: str
    content_data: Dict[str, Any]
    content_type: str
    status: str = "PENDING"
    agent_feedback: Optional[str] = None
    audit_by: Optional[str] = None
    prompt_origin: Optional[str] = None


@dataclass(frozen=True)
class UpdateContentLogData:
    # Solo los campos editables según tu requerimiento
    status: Optional[str] = None
    agent_feedback: Optional[str] = None
    audit_by: Optional[str] = None
