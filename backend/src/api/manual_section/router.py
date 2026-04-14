from fastapi import APIRouter, Depends


from dddpy.manual_section.usecase.manual_section_usecase import ManualSectionUseCase
from dddpy.auth.usecase.auth_checker_service import AuthChecker

router = APIRouter()


from dddpy.shared.logging.logging import Logger

logging = Logger("routing_usecase")


@router.get(
    "/list",
    dependencies=[Depends(AuthChecker())],
)
async def get_all():
    logging.info("list_manual_section Route")
    result_manual_section = await ManualSectionUseCase().list_all()
    return result_manual_section


@router.get(
    "/get_by_id/{id_manual_section}",
    dependencies=[Depends(AuthChecker())],
)
async def get_by_id(id_manual_section: str):
    result_manual_section = await ManualSectionUseCase().get_by_id(id_manual_section)
    return result_manual_section
