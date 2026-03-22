from fastapi import APIRouter, Depends

from dddpy.content_log.usecase.content_log_cmd_schema import (
    UpdateContentLogSchema,
    CreateContentLogSchema,
)
from dddpy.content_log.usecase.content_log_usecase import ContentLogUseCase


# from dddpy.shared.security.require_roles_and_permissions import require_permissions

router = APIRouter()


from dddpy.shared.logging.logging import Logger

logging = Logger("routing_usecase")


@router.get(
    "/list",
)
def get_all():
    logging.info("list_content_log Route")
    logging.info("Listing all content_log")
    result_content_log = ContentLogUseCase().list_all()
    return result_content_log


@router.post("/create")
def create(new_content_log: CreateContentLogSchema):
    logging.info("create_content_log Route")
    logging.info("Creating new content_log")
    response = ContentLogUseCase().create(new_content_log)
    return response.dict()


@router.get("/get_by_id/{id_content_log}")
def get_by_id(id_content_log: str):
    result_content_log = ContentLogUseCase().get_by_id(id_content_log)
    return result_content_log


@router.get("/get_by_content_log_name/{content_log_name}")
def get_by_content_log_name(content_log_name: str):
    result_content_log = ContentLogUseCase().get_by_content_log_name(content_log_name)
    return result_content_log


@router.put("/update/{content_log_id}")
def update(content_log_id: str, content_log: UpdateContentLogSchema):
    result_content_log = ContentLogUseCase().update(content_log_id, content_log)
    return result_content_log


@router.delete("/delete/{content_log_id}")
def delete(content_log_id: str):
    result_content_log = ContentLogUseCase().delete(content_log_id)
    return result_content_log
