from dddpy.manual_record.infrastructure.manual_record_cmd_repository import (
    ManualRecordCmdRepositoryImpl,
)
from dddpy.manual_record.infrastructure.manual_record_query_repository import (
    ManualRecordQueryRepositoryImpl,
)
from dddpy.manual_record.usecase.manual_record_cmd_usecase import ManualRecordCmdUseCase
from dddpy.manual_record.usecase.manual_record_query_usecase import (
    ManualRecordQueryUseCase,
)


def manual_record_cmd_usecase_factory():
    repository = ManualRecordCmdRepositoryImpl()
    return ManualRecordCmdUseCase(repository)


def manual_record_query_usecase_factory():
    repository = ManualRecordQueryRepositoryImpl()
    return ManualRecordQueryUseCase(repository)
