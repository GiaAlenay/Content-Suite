from fastapi import APIRouter, Depends

from dddpy.brand_manual_vector.usecase.brand_manual_vector_cmd_schema import (
    UpdateBrandManualVectorSchema,
    CreateBrandManualVectorSchema,
)
from dddpy.brand_manual_vector.usecase.brand_manual_vector_usecase import (
    BrandManualVectorUseCase,
)


# from dddpy.shared.security.require_roles_and_permissions import require_permissions

router = APIRouter()


from dddpy.shared.logging.logging import Logger

logging = Logger("routing_usecase")


# @router.get(
#     "/list",
#     dependencies=[
#         Depends(require_permissions(["backAdmin:brand_manual_vector.read", "intranet:brand_manual_vector.read"]))
#     ],
# )
# def get_all():
#     logging.info("list_brand_manual_vector Route")
#     logging.info("Listing all brand_manual_vector")
#     result_brand_manual_vector = BrandManualVectorUseCase().list_all()
#     return result_brand_manual_vector


# @router.post(
#     "/create", dependencies=[Depends(require_permissions(["backAdmin:brand_manual_vector.create"]))]
# )
# def create(new_brand_manual_vector: CreateBrandManualVectorSchema):
#     logging.info("create_brand_manual_vector Route")
#     logging.info("Creating new brand_manual_vector")
#     response = BrandManualVectorUseCase().create(new_brand_manual_vector)
#     return response.dict()


# @router.get(
#     "/get_by_id/{id_brand_manual_vector}",
#     dependencies=[Depends(require_permissions(["backAdmin:brand_manual_vector.read"]))],
# )
# def get_by_id(id_brand_manual_vector: int):
#     result_brand_manual_vector = BrandManualVectorUseCase().get_by_id(id_brand_manual_vector)
#     return result_brand_manual_vector


# @router.get(
#     "/get_by_brand_manual_vector_name/{brand_manual_vector_name}",
#     dependencies=[Depends(require_permissions(["backAdmin:brand_manual_vector.read"]))],
# )
# def get_by_brand_manual_vector_name(brand_manual_vector_name: str):
#     result_brand_manual_vector = BrandManualVectorUseCase().get_by_brand_manual_vector_name(brand_manual_vector_name)
#     return result_brand_manual_vector


# @router.put(
#     "/update/{brand_manual_vector_id}",
#     dependencies=[Depends(require_permissions(["backAdmin:brand_manual_vector.read"]))],
# )
# def update(brand_manual_vector_id: str, brand_manual_vector: UpdateBrandManualVectorSchema):
#     result_brand_manual_vector = BrandManualVectorUseCase().update(brand_manual_vector_id, brand_manual_vector)
#     return result_brand_manual_vector


# @router.delete(
#     "/delete/{brand_manual_vector_id}",
#     dependencies=[Depends(require_permissions(["backAdmin:brand_manual_vector.read"]))],
# )
# def delete(brand_manual_vector_id: str):
#     result_brand_manual_vector = BrandManualVectorUseCase().delete(brand_manual_vector_id)
#     return result_brand_manual_vector
