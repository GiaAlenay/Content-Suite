from fastapi import APIRouter, Depends
from dddpy.auth.usecase.auth_cmd_schema import UserRole
from typing import Dict, Any
from dddpy.manual_generator.usecase.manual_generator_usecase import (
    ManualGeneratorUseCase,
)
from dddpy.auth.usecase.auth_checker_service import AuthChecker

router = APIRouter()


from dddpy.shared.logging.logging import Logger

logging = Logger("ManualGenerator_router")


@router.post("/create/{id_brand}")
def create(
    id_brand: str,
    raw_parameters: Dict[str, Any],
    current_user: dict = Depends(AuthChecker([UserRole.ADMIN])),
):
    logging.info(
        f"Create Manual route for brand: {id_brand} and current_user={current_user}"
    )
    response = ManualGeneratorUseCase().excecute(
        brand_id=id_brand, raw_parameters=raw_parameters, user_id=current_user["id"]
    )
    return response
