from fastapi import APIRouter, Depends


from dddpy.chat_history.usecase.chat_history_usecase import ChatHistoryUseCase
from dddpy.auth.usecase.auth_checker_service import AuthChecker

router = APIRouter()


from dddpy.shared.logging.logging import Logger

logging = Logger("routing_usecase")


@router.get(
    "/list",
    dependencies=[Depends(AuthChecker())],
)
async def get_all():
    logging.info("list_chat_history Route")
    result_chat_history = await ChatHistoryUseCase().list_all()
    return result_chat_history


@router.get(
    "/get_by_id/{id_chat_history}",
    dependencies=[Depends(AuthChecker())],
)
async def get_by_id(id_chat_history: str):
    result_chat_history = await ChatHistoryUseCase().get_by_id(id_chat_history)
    return result_chat_history
