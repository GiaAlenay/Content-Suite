from abc import ABC, abstractmethod
from typing import Optional, List

from dddpy.chat_session.domain.chat_session_entity import ChatSessionEntity


class ChatSessionQueryRepository(ABC):

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[ChatSessionEntity]:
        pass

    @abstractmethod
    async def get_current_version_by_brand_id(
        self, brand_id: str
    ) -> Optional[ChatSessionEntity]:
        pass

    @abstractmethod
    async def get_by_chat_session_brand_id(
        self, chat_session_brand_id: str
    ) -> List[ChatSessionEntity]:
        pass

    @abstractmethod
    async def list_all(self) -> List[ChatSessionEntity]:
        pass
