from dddpy.chat_session.usecase.chat_session_cmd_usecase import ChatSessionCmdUseCase
from dddpy.chat_session.usecase.chat_session_query_usecase import (
    ChatSessionQueryUseCase,
)
from dddpy.chat_session.usecase.chat_session_factory import (
    chat_session_cmd_usecase_factory,
    chat_session_query_usecase_factory,
)
from dddpy.chat_session.usecase.chat_session_cmd_schema import (
    CreateChatSessionSchema,
    UpdateChatSessionSchema,
)

from dddpy.shared.schemas.response_schema import (
    ResponseSuccessSchema,
)

from dddpy.shared.logging.logging import Logger

logging = Logger("chat_session_usecase")

from dddpy.chat_session.domain.chat_session_exception import ChatSessionNotFound
from dddpy.chat_session.domain.chat_session_success import ChatSessionSucessMessage


class ChatSessionUseCase:
    def __init__(self):
        logging.info("__init__")
        self.chat_session_cmd_usecase: ChatSessionCmdUseCase = (
            chat_session_cmd_usecase_factory()
        )
        self.chat_session_query_usecase: ChatSessionQueryUseCase = (
            chat_session_query_usecase_factory()
        )
        logging.info("ChatSessionUseCase initialized")

    async def create(self, chat_session_data: CreateChatSessionSchema):
        logging.info("create")
        logging.info(f"Creating a new chat_session with data: {chat_session_data}")

        new_chat_session = await self.chat_session_cmd_usecase.create(chat_session_data)
        success = ResponseSuccessSchema(
            success=True,
            message=ChatSessionSucessMessage.MANUALRECORD_CREATED,
            data=new_chat_session.to_dict(),
        )
        logging.info(f"ChatSession created successfully: {success}")
        return success

    async def get_by_id(self, id: str):
        logging.info("get_by_id")
        chat_session = await self.chat_session_query_usecase.get_by_id(id)
        if not chat_session:
            raise ChatSessionNotFound()
        success = ResponseSuccessSchema(
            success=True,
            message=ChatSessionSucessMessage.MANUALRECORD_GET,
            data=chat_session.to_dict(),
        )
        logging.info(f"ChatSession retrieved successfully by id={id}")
        return success

    async def get_by_chat_session_brand_id(self, chat_session_brand_id: str):
        logging.info("get_by_chat_session_brand_id")
        chat_session = (
            await self.chat_session_query_usecase.get_by_chat_session_brand_id(
                chat_session_brand_id
            )
        )

        success = ResponseSuccessSchema(
            success=True,
            message=ChatSessionSucessMessage.MANUALRECORD_GET,
            data=chat_session.to_dict(),
        )
        logging.info(
            f"ChatSession retrieved successfully by brand_id={chat_session_brand_id}"
        )
        return success

    async def update(self, id: str, chat_session_data: UpdateChatSessionSchema):
        logging.info("update")
        logging.info(f"Updating chat_session {id} with data: {chat_session_data}")

        updated_chat_session = await self.chat_session_cmd_usecase.update(
            id, chat_session_data
        )
        if not updated_chat_session:
            raise ChatSessionNotFound()

        success = ResponseSuccessSchema(
            success=True,
            message=ChatSessionSucessMessage.MANUALRECORD_UPDATED,
            data=updated_chat_session.to_dict(),
        )
        logging.info(f"ChatSession updated successfully: {success}")
        return success

    async def list_all(self):
        logging.info("list_all")
        chat_session = await self.chat_session_query_usecase.list_all()
        success = ResponseSuccessSchema(
            success=True,
            message=ChatSessionSucessMessage.MANUALRECORDS_GET,
            data=[c.to_dict() for c in chat_session],
        )
        logging.info(
            f"ChatSessions listed successfully: {len(chat_session)} chat_session"
        )
        return success
