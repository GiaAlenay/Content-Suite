from fastapi import APIRouter, Depends
from dddpy.auth.usecase.auth_cmd_schema import UserRole
from typing import Dict, Any
from dddpy.manual_generator.usecase.manual_generator_factory import (
    manual_generator_usecase_factory,
)
from dddpy.auth.usecase.auth_checker_service import AuthChecker
from dddpy.manual_generator.usecase.manual_generator_schema import ManualRequestSchema

router = APIRouter()


from dddpy.shared.logging.logging import Logger

logging = Logger("ManualGenerator_router")


@router.post("/create/{id_brand}")
def create(
    id_brand: str,
    raw_parameters: ManualRequestSchema,
    current_user: dict = Depends(AuthChecker([UserRole.ADMIN])),
):
    logging.info(
        f"Create Manual route for brand: {id_brand} and current_user={current_user}"
    )
    response = manual_generator_usecase_factory().excecute(
        brand_id=id_brand, raw_parameters=raw_parameters, user_id=current_user["id"]
    )
    return response
