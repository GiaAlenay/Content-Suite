from fastapi import APIRouter, Depends
from dddpy.auth.usecase.auth_cmd_schema import UserRole
from dddpy.content_log.usecase.content_log_cmd_schema import (
    UpdateContentLogSchema,
    GenerateContentRequest,
)
from dddpy.content_log.usecase.content_log_usecase import ContentLogUseCase


router = APIRouter()

from dddpy.auth.usecase.auth_checker_service import AuthChecker
from dddpy.shared.logging.logging import Logger

logging = Logger("content_log router")


@router.get(
    "/list",
    dependencies=[Depends(AuthChecker())],
)
def get_all():
    logging.info("list_content_log Route")
    logging.info("Listing all content_log")
    result_content_log = ContentLogUseCase().list_all()
    return result_content_log


@router.post("/create/{brand_id}")
def create(
    brand_id: str,
    content_log_request: GenerateContentRequest,
    current_user: dict = Depends(AuthChecker([UserRole.CREATOR])),
):
    logging.info("create_content_log Route by user={current_user}")
    response = ContentLogUseCase().create(
        brand_id, content_log_request, current_user["id"]
    )
    return response.dict()


@router.get(
    "/get_by_id/{id_content_log}",
    dependencies=[Depends(AuthChecker())],
)
def get_by_id(id_content_log: str):
    result_content_log = ContentLogUseCase().get_by_id(id_content_log)
    return result_content_log


@router.put(
    "/auditar-texto/{content_log_id}",
    dependencies=[Depends(AuthChecker([UserRole.APPROVER_A]))],
)
def auditar_texto(content_log_id: str):
    result_content_log = ContentLogUseCase().auditar_texto(id=content_log_id)
    return result_content_log


@router.post("/auditar-imagen/{brand_id}")
async def auditar_imagen(
    brand_id: str,
    file_url: str,
    current_user: dict = Depends(AuthChecker([UserRole.APPROVER_B])),
):
    result = ContentLogUseCase().auditar_multimodal(
        brand_id=brand_id, file_url=file_url, user_id=current_user["id"]
    )
    return result


@router.put("/update_audited_information/{content_log_id}")
def update_audited_information(
    content_log_id: str,
    content_log: UpdateContentLogSchema,
    current_user: dict = Depends(
        AuthChecker([UserRole.APPROVER_A, UserRole.APPROVER_B])
    ),
):
    logging.info("update_audited_information Route by user={current_user}")
    result_content_log = ContentLogUseCase().update_audited_information(
        id=content_log_id, content_log_data=content_log, user_id=current_user["id"]
    )
    return result_content_log
