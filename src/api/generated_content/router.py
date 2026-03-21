from fastapi import APIRouter, Depends

from dddpy.generated_content.usecase.generated_content_cmd_schema import (
    UpdateGeneratedContentSchema,
    CreateGeneratedContentSchema,
)
from dddpy.generated_content.usecase.generated_content_usecase import (
    GeneratedContentUseCase,
)


# from dddpy.shared.security.require_roles_and_permissions import require_permissions

router = APIRouter()


from dddpy.shared.logging.logging import Logger

logging = Logger("routing_usecase")


# @router.get(
#     "/list",
#     dependencies=[
#         Depends(require_permissions(["backAdmin:generatedcontent.read", "intranet:generatedcontent.read"]))
#     ],
# )
# def get_all():
#     logging.info("list_generatedcontent Route")
#     logging.info("Listing all generatedcontent")
#     result_generatedcontent = GeneratedContentUseCase().list_all()
#     return result_generatedcontent


# @router.post(
#     "/create", dependencies=[Depends(require_permissions(["backAdmin:generatedcontent.create"]))]
# )
# def create(new_generatedcontent: CreateGeneratedContentSchema):
#     logging.info("create_generatedcontent Route")
#     logging.info("Creating new generatedcontent")
#     response = GeneratedContentUseCase().create(new_generatedcontent)
#     return response.dict()


# @router.get(
#     "/get_by_id/{id_generatedcontent}",
#     dependencies=[Depends(require_permissions(["backAdmin:generatedcontent.read"]))],
# )
# def get_by_id(id_generatedcontent: int):
#     result_generatedcontent = GeneratedContentUseCase().get_by_id(id_generatedcontent)
#     return result_generatedcontent


# @router.get(
#     "/get_by_generatedcontent_name/{generatedcontent_name}",
#     dependencies=[Depends(require_permissions(["backAdmin:generatedcontent.read"]))],
# )
# def get_by_generatedcontent_name(generatedcontent_name: str):
#     result_generatedcontent = GeneratedContentUseCase().get_by_generatedcontent_name(generatedcontent_name)
#     return result_generatedcontent


# @router.put(
#     "/update/{generatedcontent_id}",
#     dependencies=[Depends(require_permissions(["backAdmin:generatedcontent.read"]))],
# )
# def update(generatedcontent_id: str, generatedcontent: UpdateGeneratedContentSchema):
#     result_generatedcontent = GeneratedContentUseCase().update(generatedcontent_id, generatedcontent)
#     return result_generatedcontent


# @router.delete(
#     "/delete/{generatedcontent_id}",
#     dependencies=[Depends(require_permissions(["backAdmin:generatedcontent.read"]))],
# )
# def delete(generatedcontent_id: str):
#     result_generatedcontent = GeneratedContentUseCase().delete(generatedcontent_id)
#     return result_generatedcontent
