from fastapi import APIRouter, Depends
from dddpy.auth.usecase.auth_cmd_schema import UserRole
from typing import Dict, Any
from dddpy.manual_generator.usecase.manual_generator_factory import (
    manual_generator_usecase_factory,
)
from dddpy.auth.usecase.auth_checker_service import AuthChecker
from dddpy.manual_generator.usecase.manual_generator_schema import (
    RefinementRequest,
    ManualRequestSchema,
)

router = APIRouter()


from dddpy.shared.logging.logging import Logger

logging = Logger("ManualGenerator_router")


# @router.post("/create/{id_brand}")
# async def create(
#     id_brand: str,
#     raw_parameters: ManualRequestSchema,
#     current_user: dict = Depends(AuthChecker([UserRole.ADMIN])),
# ):
#     logging.info(
#         f"Create Manual route for brand: {id_brand} and current_user={current_user}"
#     )
#     response = manual_generator_usecase_factory().excecute(
#         brand_id=id_brand, raw_parameters=raw_parameters, user_id=current_user["id"]
#     )
#     return response


@router.post(
    "/audit/{id_brand}",
    dependencies=[Depends(AuthChecker(UserRole.ADMIN))],
)
async def audit(
    id_brand: str,
    raw_parameters: ManualRequestSchema,
):
    response = await manual_generator_usecase_factory().audit_and_generate(
        brand_id=id_brand, raw_parameters=raw_parameters
    )
    return response


@router.post(
    "/refine/{manual_id}",
    dependencies=[Depends(AuthChecker(UserRole.ADMIN))],
)
async def refine(
    manual_id: str,
    request: RefinementRequest,
):
    logging.info(f"Refining manual {manual_id}")
    response = await manual_generator_usecase_factory().execute_refinement(
        manual_id=manual_id, refinement_prompt=request.refinement_prompt
    )
    return response


@router.post("/confirm/{manual_id}")
async def confirm(
    manual_id: str,
    current_user: dict = Depends(AuthChecker([UserRole.ADMIN])),
):
    logging.info(f"Refining manual {manual_id}")
    response = await manual_generator_usecase_factory().confirm_manual(
        manual_id=manual_id, user_id=current_user["id"]
    )
    return response
