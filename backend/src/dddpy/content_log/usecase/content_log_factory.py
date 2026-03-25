from dddpy.content_log.infrastructure.content_log_cmd_repository import (
    ContentLogCmdRepositoryImpl,
)
from dddpy.content_log.infrastructure.content_log_query_repository import (
    ContentLogQueryRepositoryImpl,
)
from dddpy.content_log.usecase.content_log_cmd_usecase import ContentLogCmdUseCase
from dddpy.content_log.usecase.content_log_query_usecase import ContentLogQueryUseCase


def content_log_cmd_usecase_factory():
    repository = ContentLogCmdRepositoryImpl()
    return ContentLogCmdUseCase(repository)


def content_log_query_usecase_factory():
    repository = ContentLogQueryRepositoryImpl()
    return ContentLogQueryUseCase(repository)
