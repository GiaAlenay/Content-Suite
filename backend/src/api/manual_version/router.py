from fastapi import APIRouter, Depends


from dddpy.manual_version.usecase.manual_version_usecase import ManualVersionUseCase
from dddpy.auth.usecase.auth_checker_service import AuthChecker

router = APIRouter()


from dddpy.shared.logging.logging import Logger

logging = Logger("routing_usecase")


@router.get(
    "/list",
    dependencies=[Depends(AuthChecker())],
)
def get_all():
    logging.info("list_manual_version Route")
    result_manual_version = ManualVersionUseCase().list_all()
    return result_manual_version


@router.get(
    "/get_by_id/{id_manual_version}",
    dependencies=[Depends(AuthChecker())],
)
def get_by_id(id_manual_version: str):
    result_manual_version = ManualVersionUseCase().get_by_id(id_manual_version)
    return result_manual_version
