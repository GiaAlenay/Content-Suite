from dddpy.manual_version.infrastructure.manual_version_cmd_repository import (
    ManualVersionCmdRepositoryImpl,
)
from dddpy.manual_version.infrastructure.manual_version_query_repository import (
    ManualVersionQueryRepositoryImpl,
)
from dddpy.manual_version.usecase.manual_version_cmd_usecase import (
    ManualVersionCmdUseCase,
)
from dddpy.manual_version.usecase.manual_version_query_usecase import (
    ManualVersionQueryUseCase,
)


def manual_version_cmd_usecase_factory():
    repository = ManualVersionCmdRepositoryImpl()
    return ManualVersionCmdUseCase(repository)


def manual_version_query_usecase_factory():
    repository = ManualVersionQueryRepositoryImpl()
    return ManualVersionQueryUseCase(repository)
