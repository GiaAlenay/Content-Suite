from dddpy.chat_history.domain.chat_history_query_repository import (
    ChatHistoryQueryRepository,
)
from dddpy.chat_history.domain.chat_history_entity import ChatHistoryEntity

from typing import Optional, List


from dddpy.shared.logging.logging import Logger

logging = Logger("ChatHistoryQueryUseCase")


class ChatHistoryQueryUseCase:

    def __init__(self, repository: ChatHistoryQueryRepository):
        logging.info("ChatHistoryQueryUseCase initialized")
        self.repository = repository

    async def get_current_version_by_brand_id(
        self, brand_id: str
    ) -> Optional[ChatHistoryEntity]:
        logging.info(
            f"Delegating chat_history fetch by brand_id={brand_id} latest version"
        )
        return await self.repository.get_current_version_by_brand_id(brand_id)

    async def get_by_id(self, id: str) -> Optional[ChatHistoryEntity]:
        logging.info(f"Delegating chat_history fetch by id={id}")
        return await self.repository.get_by_id(id)

    async def get_by_chat_history_brand_id(
        self, chat_history_brand_id: str
    ) -> Optional[ChatHistoryEntity]:
        logging.info(
            f"Delegating chat_history fetch by brand_id={chat_history_brand_id}"
        )
        return await self.repository.get_by_chat_history_brand_id(chat_history_brand_id)

    async def list_all(self) -> List[ChatHistoryEntity]:
        logging.info("Delegating chat_history list_all")
        return await self.repository.list_all()
