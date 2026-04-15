from fastapi import APIRouter, Depends
from dddpy.auth.usecase.auth_cmd_schema import UserRole
from typing import Dict, Any
from dddpy.manual_generator.usecase.manual_generator_factory import (
    manual_generator_usecase_factory,
)

from dddpy.manual_generator.usecase.manual_generator_usecase import (
    ManualGeneratorUseCase,
)
from dddpy.auth.usecase.auth_checker_service import AuthChecker
from dddpy.manual_generator.usecase.manual_generator_schema import (
    RefinementRequest,
    ManualRequestSchema,
    ChatRequest,
)

router = APIRouter()


from dddpy.shared.logging.logging import Logger

logging = Logger("ManualGenerator_router")


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


@router.post("/init/{brand_id}")
async def initialize(
    brand_id: str,
    request: ManualRequestSchema,
    use_case: ManualGeneratorUseCase = Depends(manual_generator_usecase_factory),
):
    return await use_case.initialize_generation(brand_id, request)


@router.post("/chat")
async def chat_refinement(
    request: ChatRequest,
    use_case: ManualGeneratorUseCase = Depends(manual_generator_usecase_factory),
):
    response = await use_case.process_chat_interaction(
        brand_id=request.brand_id, user_id=request.user_id, message=request.message
    )
    return response


@router.post("/approve/{brand_id}")
async def approve_manual(
    brand_id: str,
    use_case: ManualGeneratorUseCase = Depends(manual_generator_usecase_factory),
):
    result = await use_case.approve_and_finalize(brand_id=brand_id)
    return result
