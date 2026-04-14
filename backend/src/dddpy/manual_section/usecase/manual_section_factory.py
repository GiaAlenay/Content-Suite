from dddpy.manual_section.infrastructure.manual_section_cmd_repository import (
    ManualSectionCmdRepositoryImpl,
)
from dddpy.manual_section.infrastructure.manual_section_query_repository import (
    ManualSectionQueryRepositoryImpl,
)
from dddpy.manual_section.usecase.manual_section_cmd_usecase import ManualSectionCmdUseCase
from dddpy.manual_section.usecase.manual_section_query_usecase import (
    ManualSectionQueryUseCase,
)


def manual_section_cmd_usecase_factory():
    repository = ManualSectionCmdRepositoryImpl()
    return ManualSectionCmdUseCase(repository)


def manual_section_query_usecase_factory():
    repository = ManualSectionQueryRepositoryImpl()
    return ManualSectionQueryUseCase(repository)
