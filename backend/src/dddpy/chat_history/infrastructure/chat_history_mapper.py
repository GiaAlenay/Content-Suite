from dddpy.chat_history.domain.chat_history_entity import ChatHistoryEntity
from dddpy.chat_history.domain.chat_history_data import CreateChatHistoryData


class ChatHistoryMapper:
    @staticmethod
    def to_domain(db_dict: dict) -> ChatHistoryEntity:
        return ChatHistoryEntity(
            id=db_dict.get("id"),
            session_id=db_dict.get("session_id"),
            manual_version_id=db_dict.get("manual_version_id"),
            role=db_dict.get("role"),
            content=db_dict.get("content"),
            order_number=db_dict.get("order_number"),
            metadata=db_dict.get("metadata", {}),
            created_at=db_dict.get("created_at"),
            updated_at=db_dict.get("updated_at"),
        )

    @staticmethod
    def to_infrastructure_from_create(data: CreateChatHistoryData) -> dict:
        return {
            "session_id": data.session_id,
            "manual_version_id": data.manual_version_id,
            "role": data.role,
            "content": data.content,
            "metadata": data.metadata or {},
            "order_number": data.order_number,
        }
