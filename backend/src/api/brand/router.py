from fastapi import APIRouter, Depends

from dddpy.brand.usecase.brand_cmd_schema import (
    UpdateBrandSchema,
    CreateBrandSchema,
)
from dddpy.brand.usecase.brand_usecase import BrandUseCase
from dddpy.auth.usecase.auth_cmd_schema import UserRole

router = APIRouter()

from dddpy.auth.usecase.auth_checker_service import AuthChecker
from dddpy.shared.logging.logging import Logger

logging = Logger("brand router")


@router.get("/list", dependencies=[Depends(AuthChecker())])
async def get_all():
    logging.info("list_brand Route")
    result_brand = await BrandUseCase().list_all()
    return result_brand


@router.get("/list_active_with_current_manual", dependencies=[Depends(AuthChecker())])
async def list_active_with_current_manual():
    logging.info("list_active_with_current_manual Route")
    result_brand = await BrandUseCase().list_active_with_current_manual()
    return result_brand


@router.post("/create", dependencies=[Depends(AuthChecker([UserRole.ADMIN]))])
async def create(new_brand: CreateBrandSchema):
    logging.info("create_brand Route")
    result_brand = await BrandUseCase().create(new_brand)
    return result_brand


@router.get(
    "/get_by_id/{id_brand}",
    dependencies=[Depends(AuthChecker())],
)
async def get_by_id(id_brand: str):
    result_brand = await BrandUseCase().get_by_id(id_brand)
    return result_brand


@router.get("/get_by_brand_name/{brand_name}", dependencies=[Depends(AuthChecker())])
async def get_by_brand_name(brand_name: str):
    result_brand = await BrandUseCase().get_by_brand_name(brand_name)
    return result_brand


@router.put("/update/{brand_id}", dependencies=[Depends(AuthChecker([UserRole.ADMIN]))])
async def update(brand_id: str, brand: UpdateBrandSchema):
    result_brand = await BrandUseCase().update(id=brand_id, brand_data=brand)
    return result_brand


@router.delete(
    "/delete/{brand_id}", dependencies=[Depends(AuthChecker([UserRole.ADMIN]))]
)
async def delete(brand_id: str):
    result_brand = await BrandUseCase().delete(brand_id)
    return result_brand
