from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class GeneratedContentgData:
    generated_content: Optional[str] = None
    llm_opinion: Optional[str] = None
    is_aligned: Optional[bool] = None
    image_url: Optional[str] = None


@dataclass(frozen=True)
class CreateContentLogData:
    brand_id: str
    creator_id: str
    content_data: GeneratedContentgData
    content_type: str
    status: str = "CREATED"
    agent_feedback: Optional[str] = None
    audit_by: Optional[str] = None
    prompt_origin: Optional[str] = None
    parent_id: Optional[str] = None


@dataclass(frozen=True)
class UpdateContentLogData:
    status: Optional[str] = None
    agent_feedback: Optional[str] = None
    audit_by: Optional[str] = None
