from typing import Annotated, List, Optional, TypedDict
from operator import add
from langchain_core.messages import BaseMessage


class ManualState(TypedDict):
    brand_id: str
    brand_name: str
    brand_description: str
    manual_version_id: Optional[str]
    chat_session_id: Optional[str]
    raw_params: dict

    audit_report: Optional[dict]
    full_content: Optional[str]
    sections: List[dict]

    messages: Annotated[List[BaseMessage], add]

    next_step: str
