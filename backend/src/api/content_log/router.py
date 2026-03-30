from fastapi import APIRouter, Depends
from dddpy.auth.usecase.auth_cmd_schema import UserRole
from dddpy.content_log.usecase.content_log_cmd_schema import (
    UpdateContentLogSchema,
    GenerateContentRequest,
)

from dddpy.auth.usecase.auth_checker_service import AuthChecker
from dddpy.shared.logging.logging import Logger

router = APIRouter()


logging = Logger("content_log router")


from dddpy.content_log.usecase.content_log_factory import content_log_usecase_factory


@router.get("/list_me")
def get_list_me(
    current_user: dict = Depends(AuthChecker([UserRole.CREATOR])),
):
    logging.info("Listing all content_log")

    usecase = content_log_usecase_factory()
    result_content_log = usecase.get_list_me(
        user_role=current_user["role"], user_id=current_user["id"]
    )
    return result_content_log


@router.post("/create/{brand_id}")
def create(
    brand_id: str,
    content_log_request: GenerateContentRequest,
    current_user: dict = Depends(AuthChecker([UserRole.CREATOR])),
):
    logging.info("create_content_log Route by user={current_user}")
    usecase = content_log_usecase_factory()
    response = usecase.create(brand_id, content_log_request, current_user["id"])
    return response.dict()


@router.get(
    "/get_by_id/{id_content_log}",
    dependencies=[Depends(AuthChecker())],
)
def get_by_id(id_content_log: str):
    usecase = content_log_usecase_factory()
    result_content_log = usecase.get_by_id(id_content_log)
    return result_content_log


@router.put(
    "/auditar-texto/{content_log_id}",
    dependencies=[Depends(AuthChecker([UserRole.APPROVER_A]))],
)
def auditar_texto(content_log_id: str):
    usecase = content_log_usecase_factory()
    result_content_log = usecase.auditar_texto(id=content_log_id)
    return result_content_log


@router.post("/auditar-imagen/{brand_id}")
async def auditar_imagen(
    brand_id: str,
    file_url: str,
    current_user: dict = Depends(AuthChecker([UserRole.APPROVER_B])),
):
    usecase = content_log_usecase_factory()
    result = usecase.auditar_multimodal(
        brand_id=brand_id, file_url=file_url, user_id=current_user["id"]
    )
    return result


@router.put("/update/{content_log_id}")
def update_audited_information(
    content_log_id: str,
    content_log: UpdateContentLogSchema,
    current_user: dict = Depends(
        AuthChecker([UserRole.APPROVER_A, UserRole.APPROVER_B])
    ),
):
    logging.info("update_audited_information Route by user={current_user}")
    usecase = content_log_usecase_factory()
    result_content_log = usecase.update_audited_information(
        id=content_log_id, content_log_data=content_log, user_id=current_user["id"]
    )
    return result_content_log
