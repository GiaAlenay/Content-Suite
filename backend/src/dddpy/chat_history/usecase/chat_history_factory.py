from dddpy.chat_history.infrastructure.chat_history_cmd_repository import (
    ChatHistoryCmdRepositoryImpl,
)
from dddpy.chat_history.infrastructure.chat_history_query_repository import (
    ChatHistoryQueryRepositoryImpl,
)
from dddpy.chat_history.usecase.chat_history_cmd_usecase import ChatHistoryCmdUseCase
from dddpy.chat_history.usecase.chat_history_query_usecase import (
    ChatHistoryQueryUseCase,
)


def chat_history_cmd_usecase_factory():
    repository = ChatHistoryCmdRepositoryImpl()
    return ChatHistoryCmdUseCase(repository)


def chat_history_query_usecase_factory():
    repository = ChatHistoryQueryRepositoryImpl()
    return ChatHistoryQueryUseCase(repository)
