from fastapi import APIRouter, Depends


from dddpy.chat_session.usecase.chat_session_usecase import ChatSessionUseCase
from dddpy.auth.usecase.auth_checker_service import AuthChecker

router = APIRouter()


from dddpy.shared.logging.logging import Logger

logging = Logger("routing_usecase")


@router.get(
    "/list",
    dependencies=[Depends(AuthChecker())],
)
async def get_all():
    logging.info("list_chat_session Route")
    result_chat_session = await ChatSessionUseCase().list_all()
    return result_chat_session


@router.get(
    "/get_by_id/{id_chat_session}",
    dependencies=[Depends(AuthChecker())],
)
async def get_by_id(id_chat_session: str):
    result_chat_session = await ChatSessionUseCase().get_by_id(id_chat_session)
    return result_chat_session
