from fastapi import APIRouter, Depends

from typing import Dict, Any
from dddpy.manual_generator.usecase.manual_generator_usecase import (
    ManualGeneratorUseCase,
)


router = APIRouter()


from dddpy.shared.logging.logging import Logger

logging = Logger("ManualGenerator_router")


@router.post("/create/{id_brand}")
def create(id_brand: str, raw_parameters: Dict[str, Any]):
    logging.info(f"Create Manual route for brand: {id_brand}")
    response = ManualGeneratorUseCase().excecute(
        brand_id=id_brand, raw_parameters=raw_parameters
    )
    return response
