from fastapi import APIRouter, Depends

from dddpy.brand.usecase.brand_cmd_schema import (
    UpdateBrandSchema,
    CreateBrandSchema,
)
from dddpy.brand.usecase.brand_usecase import BrandUseCase


# from dddpy.shared.security.require_roles_and_permissions import require_permissions

router = APIRouter()


from dddpy.shared.logging.logging import Logger

logging = Logger("routing_usecase")


# @router.get(
#     "/list",
#     dependencies=[
#         Depends(require_permissions(["backAdmin:brand.read", "intranet:brand.read"]))
#     ],
# )
# def get_all():
#     logging.add_inside_method("list_brand Route")
#     logging.info("Listing all brand")
#     result_brand = BrandUseCase().list_all()
#     return result_brand


# @router.post(
#     "/create", dependencies=[Depends(require_permissions(["backAdmin:brand.create"]))]
# )
# def create(new_brand: CreateBrandSchema):
#     logging.add_inside_method("create_brand Route")
#     logging.info("Creating new brand")
#     response = BrandUseCase().create(new_brand)
#     return response.dict()


# @router.get(
#     "/get_by_id/{id_brand}",
#     dependencies=[Depends(require_permissions(["backAdmin:brand.read"]))],
# )
# def get_by_id(id_brand: int):
#     result_brand = BrandUseCase().get_by_id(id_brand)
#     return result_brand


# @router.get(
#     "/get_by_brand_name/{brand_name}",
#     dependencies=[Depends(require_permissions(["backAdmin:brand.read"]))],
# )
# def get_by_brand_name(brand_name: str):
#     result_brand = BrandUseCase().get_by_brand_name(brand_name)
#     return result_brand


# @router.put(
#     "/update/{brand_id}",
#     dependencies=[Depends(require_permissions(["backAdmin:brand.read"]))],
# )
# def update(brand_id: int, brand: UpdateBrandSchema):
#     result_brand = BrandUseCase().update(brand_id, brand)
#     return result_brand


# @router.delete(
#     "/delete/{brand_id}",
#     dependencies=[Depends(require_permissions(["backAdmin:brand.read"]))],
# )
# def delete(brand_id: int):
#     result_brand = BrandUseCase().delete(brand_id)
#     return result_brand
