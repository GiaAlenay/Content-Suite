from fastapi import APIRouter, Depends

from dddpy.manual_record.usecase.manual_record_cmd_schema import (
    UpdateManualRecordSchema,
    CreateManualRecordSchema,
)
from dddpy.manual_record.usecase.manual_record_usecase import ManualRecordUseCase


# from dddpy.shared.security.require_roles_and_permissions import require_permissions

router = APIRouter()


from dddpy.shared.logging.logging import Logger

logging = Logger("routing_usecase")


# @router.get(
#     "/list",
#     dependencies=[
#         Depends(require_permissions(["backAdmin:manual_record.read", "intranet:manual_record.read"]))
#     ],
# )
# def get_all():
#     logging.info("list_manual_record Route")
#     logging.info("Listing all manual_record")
#     result_manual_record = ManualRecordUseCase().list_all()
#     return result_manual_record


# @router.post(
#     "/create", dependencies=[Depends(require_permissions(["backAdmin:manual_record.create"]))]
# )
# def create(new_manual_record: CreateManualRecordSchema):
#     logging.info("create_manual_record Route")
#     logging.info("Creating new manual_record")
#     response = ManualRecordUseCase().create(new_manual_record)
#     return response.dict()


# @router.get(
#     "/get_by_id/{id_manual_record}",
#     dependencies=[Depends(require_permissions(["backAdmin:manual_record.read"]))],
# )
# def get_by_id(id_manual_record: int):
#     result_manual_record = ManualRecordUseCase().get_by_id(id_manual_record)
#     return result_manual_record


# @router.get(
#     "/get_by_manual_record_name/{manual_record_name}",
#     dependencies=[Depends(require_permissions(["backAdmin:manual_record.read"]))],
# )
# def get_by_manual_record_name(manual_record_name: str):
#     result_manual_record = ManualRecordUseCase().get_by_manual_record_name(manual_record_name)
#     return result_manual_record


# @router.put(
#     "/update/{manual_record_id}",
#     dependencies=[Depends(require_permissions(["backAdmin:manual_record.read"]))],
# )
# def update(manual_record_id: str, manual_record: UpdateManualRecordSchema):
#     result_manual_record = ManualRecordUseCase().update(manual_record_id, manual_record)
#     return result_manual_record


# @router.delete(
#     "/delete/{manual_record_id}",
#     dependencies=[Depends(require_permissions(["backAdmin:manual_record.read"]))],
# )
# def delete(manual_record_id: str):
#     result_manual_record = ManualRecordUseCase().delete(manual_record_id)
#     return result_manual_record
