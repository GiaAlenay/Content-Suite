from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class CreateManualRecordData:
    brand_id: str
    version: int
    full_manual: str
    raw_parameters: Dict[str, Any]
    is_current_version: bool = True
    url_manual: Optional[str] = None
    agent_feedback: Optional[Dict[str, Any]] = None


@dataclass(frozen=True)
class UpdateManualRecordData:
    is_current_version: Optional[bool] = None
    url_manual: Optional[str] = None
    agent_feedback: Optional[Dict[str, Any]] = None
