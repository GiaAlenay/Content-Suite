from fastapi import APIRouter, Depends

from dddpy.generated_content.usecase.generated_content_cmd_schema import (
    UpdateGeneratedContentSchema,
    CreateGeneratedContentSchema,
)
from dddpy.generated_content.usecase.generated_content_usecase import (
    GeneratedContentUseCase,
)


router = APIRouter()


from dddpy.shared.logging.logging import Logger

logging = Logger("routing_usecase")


@router.get(
    "/list",
)
def get_all():
    logging.info("Listing all generatedcontent")
    result_generatedcontent = GeneratedContentUseCase().list_all()
    return result_generatedcontent


@router.post("/create")
def create(new_generatedcontent: CreateGeneratedContentSchema):
    logging.info("Creating new generatedcontent")
    response = GeneratedContentUseCase().create(new_generatedcontent)
    return response.dict()


@router.get(
    "/get_by_id/{id_generatedcontent}",
)
def get_by_id(id_generatedcontent: str):
    result_generatedcontent = GeneratedContentUseCase().get_by_id(id_generatedcontent)
    return result_generatedcontent


@router.get(
    "/get_by_generatedcontent_name/{generatedcontent_name}",
)
def get_by_generatedcontent_name(generatedcontent_name: str):
    result_generatedcontent = GeneratedContentUseCase().get_by_generatedcontent_name(
        generatedcontent_name
    )
    return result_generatedcontent


@router.put(
    "/update/{generatedcontent_id}",
)
def update(generatedcontent_id: str, generatedcontent: UpdateGeneratedContentSchema):
    result_generatedcontent = GeneratedContentUseCase().update(
        generatedcontent_id, generatedcontent
    )
    return result_generatedcontent


@router.delete(
    "/delete/{generatedcontent_id}",
)
def delete(generatedcontent_id: str):
    result_generatedcontent = GeneratedContentUseCase().delete(generatedcontent_id)
    return result_generatedcontent
