from dddpy.chat_history.usecase.chat_history_cmd_schema import (
    CreateChatHistorySchema,
)
from dddpy.chat_history.domain.chat_history_data import (
    CreateChatHistoryData,
)

from dddpy.chat_history.domain.chat_history_cmd_repository import (
    ChatHistoryCmdRepository,
)

from dddpy.shared.logging.logging import Logger

logging = Logger("ChatHistoryCmdUseCase")


class ChatHistoryCmdUseCase:

    def __init__(self, repository: ChatHistoryCmdRepository):
        self.repository = repository
        logging.info("ChatHistoryCmdUseCase initialized")

    async def create(self, chat_history_data: CreateChatHistorySchema):
        logging.info(
            f"Delegating chat_history creation for manual_version_id={chat_history_data.manual_version_id}"
        )
        data = CreateChatHistoryData(
            manual_version_id=chat_history_data.manual_version_id,
            session_id=chat_history_data.session_id,
            role=chat_history_data.role,
            content=chat_history_data.content,
            metadata=chat_history_data.metadata or {},
            order_number=chat_history_data.order_number,
        )

        return await self.repository.create(data)
