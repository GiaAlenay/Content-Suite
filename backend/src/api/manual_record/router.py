from fastapi import APIRouter, Depends


from dddpy.manual_record.usecase.manual_record_usecase import ManualRecordUseCase
from dddpy.auth.usecase.auth_checker_service import AuthChecker

router = APIRouter()


from dddpy.shared.logging.logging import Logger

logging = Logger("routing_usecase")


@router.get(
    "/list",
    dependencies=[Depends(AuthChecker())],
)
async def get_all():
    logging.info("list_manual_record Route")
    result_manual_record = await ManualRecordUseCase().list_all()
    return result_manual_record


@router.get(
    "/get_by_id/{id_manual_record}",
    dependencies=[Depends(AuthChecker())],
)
async def get_by_id(id_manual_record: str):
    result_manual_record = await ManualRecordUseCase().get_by_id(id_manual_record)
    return result_manual_record
