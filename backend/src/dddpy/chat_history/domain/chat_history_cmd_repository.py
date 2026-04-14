from abc import ABC, abstractmethod
from typing import Optional
from dddpy.chat_history.domain.chat_history_entity import ChatHistoryEntity
from dddpy.chat_history.domain.chat_history_data import (
    CreateChatHistoryData,
    UpdateChatHistoryData,
)


class ChatHistoryCmdRepository(ABC):

    @abstractmethod
    async def create(self, chat_history: CreateChatHistoryData) -> ChatHistoryEntity:
        pass

    @abstractmethod
    async def update(
        self, id: str, chat_history: UpdateChatHistoryData
    ) -> Optional[ChatHistoryEntity]:
        pass
