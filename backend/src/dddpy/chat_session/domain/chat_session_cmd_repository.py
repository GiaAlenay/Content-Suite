from abc import ABC, abstractmethod
from typing import Optional
from dddpy.chat_session.domain.chat_session_entity import ChatSessionEntity
from dddpy.chat_session.domain.chat_session_data import (
    CreateChatSessionData,
    UpdateChatSessionData,
)


class ChatSessionCmdRepository(ABC):

    @abstractmethod
    async def create(self, chat_session: CreateChatSessionData) -> ChatSessionEntity:
        pass

    @abstractmethod
    async def update(
        self, id: str, chat_session: UpdateChatSessionData
    ) -> Optional[ChatSessionEntity]:
        pass
