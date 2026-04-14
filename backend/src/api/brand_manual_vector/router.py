from fastapi import APIRouter, Depends, Depends

from dddpy.brand_manual_vector.usecase.brand_manual_vector_cmd_schema import (
    UpdateBrandManualVectorSchema,
    CreateBrandManualVectorSchema,
)
from dddpy.brand_manual_vector.usecase.brand_manual_vector_usecase import (
    BrandManualVectorUseCase,
)
from dddpy.auth.usecase.auth_checker_service import AuthChecker

router = APIRouter()


from dddpy.shared.logging.logging import Logger

logging = Logger("brand_manual_vector router")


@router.get(
    "/list",
    dependencies=[Depends(AuthChecker())],
)
async def get_all():
    logging.info("Listing all brand_manual_vector")
    result_brand_manual_vector = await BrandManualVectorUseCase().list_all()
    return result_brand_manual_vector


@router.get(
    "/get_by_id/{id_brand_manual_vector}",
    dependencies=[Depends(AuthChecker())],
)
async def get_by_id(id_brand_manual_vector: str):
    result_brand_manual_vector = await BrandManualVectorUseCase().get_by_id(
        id_brand_manual_vector
    )
    return result_brand_manual_vector
