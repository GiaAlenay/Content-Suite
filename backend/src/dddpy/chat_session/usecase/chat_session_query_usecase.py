from dddpy.chat_session.domain.chat_session_query_repository import (
    ChatSessionQueryRepository,
)
from dddpy.chat_session.domain.chat_session_entity import ChatSessionEntity

from typing import Optional, List


from dddpy.shared.logging.logging import Logger

logging = Logger("ChatSessionQueryUseCase")


class ChatSessionQueryUseCase:

    def __init__(self, repository: ChatSessionQueryRepository):
        logging.info("ChatSessionQueryUseCase initialized")
        self.repository = repository

    async def get_current_version_by_brand_id(
        self, brand_id: str
    ) -> Optional[ChatSessionEntity]:
        logging.info(
            f"Delegating chat_session fetch by brand_id={brand_id} latest version"
        )
        return await self.repository.get_current_version_by_brand_id(brand_id)

    async def get_by_id(self, id: str) -> Optional[ChatSessionEntity]:
        logging.info(f"Delegating chat_session fetch by id={id}")
        return await self.repository.get_by_id(id)

    async def get_by_chat_session_brand_id(
        self, chat_session_brand_id: str
    ) -> Optional[ChatSessionEntity]:
        logging.info(
            f"Delegating chat_session fetch by brand_id={chat_session_brand_id}"
        )
        return await self.repository.get_by_chat_session_brand_id(chat_session_brand_id)

    async def list_all(self) -> List[ChatSessionEntity]:
        logging.info("Delegating chat_session list_all")
        return await self.repository.list_all()
