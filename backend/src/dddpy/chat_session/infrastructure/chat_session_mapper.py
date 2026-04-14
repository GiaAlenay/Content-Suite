from dddpy.chat_session.domain.chat_session_entity import ChatSessionEntity
from dddpy.chat_session.domain.chat_session_data import (
    CreateChatSessionData,
    UpdateChatSessionData,
)


class ChatSessionMapper:
    @staticmethod
    def to_domain(db_dict: dict) -> ChatSessionEntity:
        return ChatSessionEntity(
            id=db_dict.get("id"),
            user_id=db_dict.get("user_id"),
            brand_id=db_dict.get("brand_id"),
            current_version_id=db_dict.get("current_version_id"),
            created_at=db_dict.get("created_at"),
            updated_at=db_dict.get("updated_at"),
        )

    @staticmethod
    def to_infrastructure_from_create(data: CreateChatSessionData) -> dict:
        return {
            "brand_id": data.brand_id,
            "current_version_id": data.current_version_id,
            "user_id": data.user_id,
        }

    @staticmethod
    def to_infrastructure_from_update(data: UpdateChatSessionData) -> dict:
        return {"current_version_id": data.current_version_id}
