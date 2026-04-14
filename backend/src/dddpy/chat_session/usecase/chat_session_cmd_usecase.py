from dddpy.chat_session.usecase.chat_session_cmd_schema import (
    CreateChatSessionSchema,
    UpdateChatSessionSchema,
)
from dddpy.chat_session.domain.chat_session_data import (
    CreateChatSessionData,
    UpdateChatSessionData,
)
from dddpy.chat_session.domain.chat_session_entity import ChatSessionEntity

from dddpy.chat_session.domain.chat_session_cmd_repository import (
    ChatSessionCmdRepository,
)
from typing import Optional
from dddpy.shared.logging.logging import Logger

logging = Logger("ChatSessionCmdUseCase")


class ChatSessionCmdUseCase:

    def __init__(self, repository: ChatSessionCmdRepository):
        self.repository = repository
        logging.info("ChatSessionCmdUseCase initialized")

    async def create(self, chat_session_data: CreateChatSessionSchema):
        logging.info(
            f"Delegating chat_session creation for brand_id={chat_session_data.brand_id}"
        )
        data = CreateChatSessionData(
            brand_id=chat_session_data.brand_id,
            current_version_id=chat_session_data.current_version_id,
            user_id=chat_session_data.user_id,
        )

        return await self.repository.create(data)

    async def update(
        self, id: str, chat_session_data: UpdateChatSessionSchema
    ) -> Optional[ChatSessionEntity]:
        logging.info(f"Delegating chat_session update for id={id}")
        data = UpdateChatSessionData(
            current_version_id=chat_session_data.current_version_id,
        )
        return await self.repository.update(id, data)
