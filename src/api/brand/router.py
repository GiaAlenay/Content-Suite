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
def get_all():
    logging.info("list_brand Route")
    result_brand = BrandUseCase().list_all()
    return result_brand


@router.post("/create", dependencies=[Depends(AuthChecker([UserRole.ADMIN]))])
def create(new_brand: CreateBrandSchema):
    logging.info("create_brand Route")
    response = BrandUseCase().create(new_brand)
    return response


@router.get(
    "/get_by_id/{id_brand}",
    dependencies=[Depends(AuthChecker())],
)
def get_by_id(id_brand: str):
    result_brand = BrandUseCase().get_by_id(id_brand)
    return result_brand


@router.get("/get_by_brand_name/{brand_name}", dependencies=[Depends(AuthChecker())])
def get_by_brand_name(brand_name: str):
    result_brand = BrandUseCase().get_by_brand_name(brand_name)
    return result_brand


@router.put("/update/{brand_id}", dependencies=[Depends(AuthChecker([UserRole.ADMIN]))])
def update(brand_id: str, brand: UpdateBrandSchema):
    result_brand = BrandUseCase().update(id=brand_id, brand_data=brand)
    return result_brand


@router.delete(
    "/delete/{brand_id}", dependencies=[Depends(AuthChecker([UserRole.ADMIN]))]
)
def delete(brand_id: str):
    result_brand = BrandUseCase().delete(brand_id)
    return result_brand
