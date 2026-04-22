from dddpy.chat_history.domain.chat_history_entity import ChatHistoryEntity
from dddpy.chat_history.infrastructure.chat_history_mapper import ChatHistoryMapper
from dddpy.chat_history.domain.chat_history_cmd_repository import (
    ChatHistoryCmdRepository,
)

from dddpy.chat_history.domain.chat_history_data import (
    CreateChatHistoryData,
)
from dddpy.shared.supabase.supabase_manager import supabase

from dddpy.shared.logging.logging import Logger
from typing import Optional

logging = Logger("ChatHistoryCmdRepositoryImpl")


class ChatHistoryCmdRepositoryImpl(ChatHistoryCmdRepository):
    def __init__(self):
        self._client = supabase
        self._table = "chat_history"
        logging.info("ChatHistoryCmdRepositoryImpl initialized with Supabase Client")

    async def create(
        self, chat_history: CreateChatHistoryData
    ) -> Optional[ChatHistoryEntity]:
        logging.info(f"Creating chat_history: {chat_history.brand_id}")

        try:

            data = ChatHistoryMapper.to_infrastructure_from_create(chat_history)

            response = await self._client.table(self._table).insert(data).execute()

            if not response.data:
                return None

            db_chat_history = response.data[0]
            logging.info(
                f"ChatHistory created successfully with ID: {db_chat_history['id']}",
            )

            return ChatHistoryMapper.to_domain(db_chat_history)

        except Exception as e:
            logging.error(f"Error creating chat_history in Supabase: {str(e)}")
            raise e
