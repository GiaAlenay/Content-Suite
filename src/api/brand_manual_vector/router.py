from fastapi import APIRouter, Depends

from dddpy.brand_manual_vector.usecase.brand_manual_vector_cmd_schema import (
    UpdateBrandManualVectorSchema,
    CreateBrandManualVectorSchema,
)
from dddpy.brand_manual_vector.usecase.brand_manual_vector_usecase import (
    BrandManualVectorUseCase,
)


router = APIRouter()


from dddpy.shared.logging.logging import Logger

logging = Logger("routing_usecase")


@router.get(
    "/list",
)
def get_all():
    logging.info("Listing all brand_manual_vector")
    result_brand_manual_vector = BrandManualVectorUseCase().list_all()
    return result_brand_manual_vector


@router.post("/create")
def create(new_brand_manual_vector: CreateBrandManualVectorSchema):
    logging.info("Creating new brand_manual_vector")
    response = BrandManualVectorUseCase().create(new_brand_manual_vector)
    return response.dict()


@router.get(
    "/get_by_id/{id_brand_manual_vector}",
)
def get_by_id(id_brand_manual_vector: str):
    result_brand_manual_vector = BrandManualVectorUseCase().get_by_id(
        id_brand_manual_vector
    )
    return result_brand_manual_vector


@router.get(
    "/get_by_brand_manual_vector_name/{brand_manual_vector_name}",
)
def get_by_brand_manual_vector_name(brand_manual_vector_name: str):
    result_brand_manual_vector = (
        BrandManualVectorUseCase().get_by_brand_manual_vector_name(
            brand_manual_vector_name
        )
    )
    return result_brand_manual_vector


@router.put(
    "/update/{brand_manual_vector_id}",
)
def update(
    brand_manual_vector_id: str, brand_manual_vector: UpdateBrandManualVectorSchema
):
    result_brand_manual_vector = BrandManualVectorUseCase().update(
        brand_manual_vector_id, brand_manual_vector
    )
    return result_brand_manual_vector


@router.delete(
    "/delete/{brand_id}",
)
def delete(brand_id: str):
    result_brand_manual_vector = BrandManualVectorUseCase().delete_by_brand_id(brand_id)
    return result_brand_manual_vector
