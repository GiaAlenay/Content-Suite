from fastapi import APIRouter

from dddpy.content_log.usecase.content_log_cmd_schema import (
    UpdateContentLogSchema,
    GenerateContentRequest,
)
from dddpy.content_log.usecase.content_log_usecase import ContentLogUseCase


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


@router.post("/create/{brand_id}")
def create(brand_id: str, content_log_request: GenerateContentRequest):
    logging.info("create_content_log Route")
    logging.info("Creating new content_log")
    response = ContentLogUseCase().create(brand_id, content_log_request)
    return response.dict()


@router.get("/get_by_id/{id_content_log}")
def get_by_id(id_content_log: str):
    result_content_log = ContentLogUseCase().get_by_id(id_content_log)
    return result_content_log


@router.get("/get_by_content_log_name/{content_log_name}")
def get_by_content_log_name(content_log_name: str):
    result_content_log = ContentLogUseCase().get_by_content_log_name(content_log_name)
    return result_content_log


@router.put("/auditar/{content_log_id}")
def auditar(content_log_id: str):
    result_content_log = ContentLogUseCase().auditar(content_log_id)
    return result_content_log


@router.post("/auditar-imagen/{brand_id}")
async def auditar_imagen(brand_id: str, file_url: str):
    result = ContentLogUseCase().auditar_multimodal(brand_id, file_url)
    return result


@router.put("/update/{content_log_id}")
def update(content_log_id: str, content_log: UpdateContentLogSchema):
    result_content_log = ContentLogUseCase().update(content_log_id, content_log)
    return result_content_log
