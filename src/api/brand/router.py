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

logging = Logger("brand_router")


@router.get("/list")
def get_all(
    current_user: dict = Depends(AuthChecker([UserRole.APPROVER, UserRole.ADMIN]))
):
    logging.info(f"El usuario {current_user['email']} está listando marcas")
    logging.info("list_brand Route")
    logging.info("Listing all brand")
    result_brand = BrandUseCase().list_all()
    return result_brand


@router.post("/create")
def create(new_brand: CreateBrandSchema):
    logging.info("create_brand Route")
    response = BrandUseCase().create(new_brand)
    return response


@router.get("/get_by_id/{id_brand}")
def get_by_id(id_brand: str):
    result_brand = BrandUseCase().get_by_id(id_brand)
    return result_brand


@router.get(
    "/get_by_brand_name/{brand_name}",
)
def get_by_brand_name(brand_name: str):
    result_brand = BrandUseCase().get_by_brand_name(brand_name)
    return result_brand


@router.put(
    "/update/{brand_id}",
)
def update(brand_id: str, brand: UpdateBrandSchema):
    result_brand = BrandUseCase().update(brand_id, brand)
    return result_brand


@router.delete(
    "/delete/{brand_id}",
)
def delete(brand_id: str):
    result_brand = BrandUseCase().delete(brand_id)
    return result_brand
