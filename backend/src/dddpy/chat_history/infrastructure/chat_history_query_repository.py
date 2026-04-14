from typing import Optional, List
from dddpy.chat_history.domain.chat_history_entity import ChatHistoryEntity
from dddpy.chat_history.domain.chat_history_query_repository import (
    ChatHistoryQueryRepository,
)
from dddpy.chat_history.infrastructure.chat_history_mapper import ChatHistoryMapper

from dddpy.shared.supabase.supabase_manager import supabase

from dddpy.shared.logging.logging import Logger

logging = Logger("ChatHistoryCmdRepositoryImpl")


class ChatHistoryQueryRepositoryImpl(ChatHistoryQueryRepository):

    def __init__(self):
        self._client = supabase
        self._table = "chat_history"
        logging.info("ChatHistoryQueryRepositoryImpl initialized with Supabase")

    async def get_by_id(self, id: str) -> Optional[ChatHistoryEntity]:
        logging.info(f"Fetching chat_history with id={id}")

        response = (
            self._client.table(self._table)
            .select("*")
            .eq("id", id)
            .maybe_single()
            .execute()
        )
        if not response or not response.data:
            return None

        db_chat_history = response.data
        return ChatHistoryMapper.to_domain(db_chat_history) if db_chat_history else None

    async def get_by_chat_history_brand_id(
        self, chat_history_brand_id: str
    ) -> List[ChatHistoryEntity]:
        logging.info(
            f"Fetching chat_history with chat_history_brand_id={chat_history_brand_id}"
        )

        response = (
            self._client.table(self._table)
            .select("*")
            .eq("brand_id", chat_history_brand_id)
            .execute()
        )

        db_chat_history = response.data
        return ChatHistoryMapper.to_domain(db_chat_history) if db_chat_history else None

    async def get_current_version_by_brand_id(
        self, brand_id: str
    ) -> Optional[ChatHistoryEntity]:
        logging.info(
            f"Fetching latest version of chat_history with brand_id={brand_id}"
        )

        response = (
            self._client.table(self._table)
            .select("*")
            .eq("brand_id", brand_id)
            .eq("is_current_version", True)
            .limit(1)
            .execute()
        )

        db_records = response.data

        if db_records and len(db_records) > 0:
            return ChatHistoryMapper.to_domain(db_records[0])

        return None

    async def list_all(self) -> List[ChatHistoryEntity]:
        logging.info("Fetching all  ")

        response = await self._client.table(self._table).select("*").execute()

        db_chat_historys = response.data
        return [ChatHistoryMapper.to_domain(db) for db in db_chat_historys]
