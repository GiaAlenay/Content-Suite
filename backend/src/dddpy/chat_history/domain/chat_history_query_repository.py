from abc import ABC, abstractmethod
from typing import Optional, List

from dddpy.chat_history.domain.chat_history_entity import ChatHistoryEntity


class ChatHistoryQueryRepository(ABC):

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[ChatHistoryEntity]:
        pass

    @abstractmethod
    async def get_current_version_by_brand_id(
        self, brand_id: str
    ) -> Optional[ChatHistoryEntity]:
        pass

    @abstractmethod
    async def get_by_chat_history_brand_id(
        self, chat_history_brand_id: str
    ) -> List[ChatHistoryEntity]:
        pass

    @abstractmethod
    async def list_all(self) -> List[ChatHistoryEntity]:
        pass
