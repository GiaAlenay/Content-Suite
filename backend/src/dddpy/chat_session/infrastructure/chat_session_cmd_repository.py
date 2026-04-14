from dddpy.chat_session.domain.chat_session_entity import ChatSessionEntity
from dddpy.chat_session.infrastructure.chat_session_mapper import ChatSessionMapper
from dddpy.chat_session.domain.chat_session_cmd_repository import (
    ChatSessionCmdRepository,
)

from dddpy.chat_session.domain.chat_session_data import (
    CreateChatSessionData,
    UpdateChatSessionData,
)
from dddpy.shared.supabase.supabase_manager import supabase

from dddpy.shared.logging.logging import Logger
from typing import Optional

logging = Logger("ChatSessionCmdRepositoryImpl")


class ChatSessionCmdRepositoryImpl(ChatSessionCmdRepository):
    def __init__(self):
        self._client = supabase
        self._table = "chat_sessions"
        logging.info("ChatSessionCmdRepositoryImpl initialized with Supabase Client")

    async def create(
        self, chat_session: CreateChatSessionData
    ) -> Optional[ChatSessionEntity]:
        logging.info(f"Creating chat_session: {chat_session.brand_id}")

        try:

            data = ChatSessionMapper.to_infrastructure_from_create(chat_session)

            response = await self._client.table(self._table).insert(data).execute()

            if not response.data:
                return None

            db_chat_session = response.data[0]
            logging.info(
                f"ChatSession created successfully with ID: {db_chat_session['id']}",
            )

            return ChatSessionMapper.to_domain(db_chat_session)

        except Exception as e:
            logging.error(f"Error creating chat_session in Supabase: {str(e)}")
            raise e

    async def update(
        self, chat_session_id: str, data: UpdateChatSessionData
    ) -> Optional[ChatSessionEntity]:
        logging.info(f"Updating chat_session with id={chat_session_id}")

        try:
            update_values = ChatSessionMapper.to_infrastructure_from_update(data)

            if not update_values:
                logging.warning("No hay valores para actualizar")
                return {}

            response = (
                self._client.table(self._table)
                .update(update_values)
                .eq("id", chat_session_id)
                .execute()
            )

            logging.info(f"Update success for id={chat_session_id}: {response.data}")
            return response.data

        except Exception as e:
            logging.error(f"Error al actualizar en Supabase: {str(e)}")
            raise e
