from dddpy.chat_history.usecase.chat_history_cmd_usecase import ChatHistoryCmdUseCase
from dddpy.chat_history.usecase.chat_history_query_usecase import (
    ChatHistoryQueryUseCase,
)
from dddpy.chat_history.usecase.chat_history_factory import (
    chat_history_cmd_usecase_factory,
    chat_history_query_usecase_factory,
)
from dddpy.chat_history.usecase.chat_history_cmd_schema import (
    CreateChatHistorySchema,
    UpdateChatHistorySchema,
)

from dddpy.shared.schemas.response_schema import (
    ResponseSuccessSchema,
)

from dddpy.shared.logging.logging import Logger

logging = Logger("chat_history_usecase")

from dddpy.chat_history.domain.chat_history_exception import ChatHistoryNotFound
from dddpy.chat_history.domain.chat_history_success import ChatHistorySucessMessage


class ChatHistoryUseCase:
    def __init__(self):
        logging.info("__init__")
        self.chat_history_cmd_usecase: ChatHistoryCmdUseCase = (
            chat_history_cmd_usecase_factory()
        )
        self.chat_history_query_usecase: ChatHistoryQueryUseCase = (
            chat_history_query_usecase_factory()
        )
        logging.info("ChatHistoryUseCase initialized")

    async def create(self, chat_history_data: CreateChatHistorySchema):
        logging.info("create")
        logging.info(f"Creating a new chat_history with data: {chat_history_data}")

        new_chat_history = await self.chat_history_cmd_usecase.create(chat_history_data)
        success = ResponseSuccessSchema(
            success=True,
            message=ChatHistorySucessMessage.MANUALRECORD_CREATED,
            data=new_chat_history.to_dict(),
        )
        logging.info(f"ChatHistory created successfully: {success}")
        return success

    async def get_by_id(self, id: str):
        logging.info("get_by_id")
        chat_history = await self.chat_history_query_usecase.get_by_id(id)
        if not chat_history:
            raise ChatHistoryNotFound()
        success = ResponseSuccessSchema(
            success=True,
            message=ChatHistorySucessMessage.MANUALRECORD_GET,
            data=chat_history.to_dict(),
        )
        logging.info(f"ChatHistory retrieved successfully by id={id}")
        return success

    async def get_by_chat_history_brand_id(self, chat_history_brand_id: str):
        logging.info("get_by_chat_history_brand_id")
        chat_history = (
            await self.chat_history_query_usecase.get_by_chat_history_brand_id(
                chat_history_brand_id
            )
        )

        success = ResponseSuccessSchema(
            success=True,
            message=ChatHistorySucessMessage.MANUALRECORD_GET,
            data=chat_history.to_dict(),
        )
        logging.info(
            f"ChatHistory retrieved successfully by brand_id={chat_history_brand_id}"
        )
        return success

    async def update(self, id: str, chat_history_data: UpdateChatHistorySchema):
        logging.info("update")
        logging.info(f"Updating chat_history {id} with data: {chat_history_data}")

        updated_chat_history = await self.chat_history_cmd_usecase.update(
            id, chat_history_data
        )
        if not updated_chat_history:
            raise ChatHistoryNotFound()

        success = ResponseSuccessSchema(
            success=True,
            message=ChatHistorySucessMessage.MANUALRECORD_UPDATED,
            data=updated_chat_history.to_dict(),
        )
        logging.info(f"ChatHistory updated successfully: {success}")
        return success

    async def list_all(self):
        logging.info("list_all")
        chat_history = await self.chat_history_query_usecase.list_all()
        success = ResponseSuccessSchema(
            success=True,
            message=ChatHistorySucessMessage.MANUALRECORDS_GET,
            data=[c.to_dict() for c in chat_history],
        )
        logging.info(
            f"ChatHistorys listed successfully: {len(chat_history)} chat_history"
        )
        return success
