from typing import Optional, List
from dddpy.chat_session.domain.chat_session_entity import ChatSessionEntity
from dddpy.chat_session.domain.chat_session_query_repository import (
    ChatSessionQueryRepository,
)
from dddpy.chat_session.infrastructure.chat_session_mapper import ChatSessionMapper

from dddpy.shared.supabase.supabase_manager import supabase

from dddpy.shared.logging.logging import Logger

logging = Logger("ChatSessionCmdRepositoryImpl")


class ChatSessionQueryRepositoryImpl(ChatSessionQueryRepository):

    def __init__(self):
        self._client = supabase
        self._table = "chat_sessions"
        logging.info("ChatSessionQueryRepositoryImpl initialized with Supabase")

    async def get_by_id(self, id: str) -> Optional[ChatSessionEntity]:
        logging.info(f"Fetching chat_session with id={id}")

        response = (
            self._client.table(self._table)
            .select("*")
            .eq("id", id)
            .maybe_single()
            .execute()
        )
        if not response or not response.data:
            return None

        db_chat_session = response.data
        return ChatSessionMapper.to_domain(db_chat_session) if db_chat_session else None

    async def get_by_chat_session_brand_id(
        self, chat_session_brand_id: str
    ) -> List[ChatSessionEntity]:
        logging.info(
            f"Fetching chat_session with chat_session_brand_id={chat_session_brand_id}"
        )

        response = (
            self._client.table(self._table)
            .select("*")
            .eq("brand_id", chat_session_brand_id)
            .execute()
        )

        db_chat_session = response.data
        return ChatSessionMapper.to_domain(db_chat_session) if db_chat_session else None

    async def get_current_version_by_brand_id(
        self, brand_id: str
    ) -> Optional[ChatSessionEntity]:
        logging.info(
            f"Fetching latest version of chat_session with brand_id={brand_id}"
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
            return ChatSessionMapper.to_domain(db_records[0])

        return None

    async def list_all(self) -> List[ChatSessionEntity]:
        logging.info("Fetching all  ")

        response = await self._client.table(self._table).select("*").execute()

        db_chat_sessions = response.data
        return [ChatSessionMapper.to_domain(db) for db in db_chat_sessions]
