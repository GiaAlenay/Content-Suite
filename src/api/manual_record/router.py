from fastapi import APIRouter, Depends


from dddpy.manual_record.usecase.manual_record_usecase import ManualRecordUseCase


router = APIRouter()


from dddpy.shared.logging.logging import Logger

logging = Logger("routing_usecase")


@router.get(
    "/list",
)
def get_all():
    logging.info("list_manual_record Route")
    result_manual_record = ManualRecordUseCase().list_all()
    return result_manual_record


@router.get(
    "/get_by_id/{id_manual_record}",
)
def get_by_id(id_manual_record: str):
    result_manual_record = ManualRecordUseCase().get_by_id(id_manual_record)
    return result_manual_record
