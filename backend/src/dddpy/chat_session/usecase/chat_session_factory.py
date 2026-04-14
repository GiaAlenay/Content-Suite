from dddpy.chat_session.infrastructure.chat_session_cmd_repository import (
    ChatSessionCmdRepositoryImpl,
)
from dddpy.chat_session.infrastructure.chat_session_query_repository import (
    ChatSessionQueryRepositoryImpl,
)
from dddpy.chat_session.usecase.chat_session_cmd_usecase import ChatSessionCmdUseCase
from dddpy.chat_session.usecase.chat_session_query_usecase import (
    ChatSessionQueryUseCase,
)


def chat_session_cmd_usecase_factory():
    repository = ChatSessionCmdRepositoryImpl()
    return ChatSessionCmdUseCase(repository)


def chat_session_query_usecase_factory():
    repository = ChatSessionQueryRepositoryImpl()
    return ChatSessionQueryUseCase(repository)
