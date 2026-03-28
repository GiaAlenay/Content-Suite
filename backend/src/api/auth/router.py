from fastapi import APIRouter
from dddpy.auth.usecase.auth_cmd_schema import RegisterSchema, LoginSchema

from dddpy.auth.usecase.auth_usecase import AuthUsecase


router = APIRouter()


from dddpy.shared.logging.logging import Logger

logging = Logger("auth_router")


@router.post("/auth/login")
async def login(credentials: LoginSchema):  # Define un pydantic schema simple
    return AuthUsecase().login(credentials.email, credentials.password)


@router.post("/auth/register")
async def register(data: RegisterSchema):
    # Aquí podrías poner una lógica para que solo el primer ADMIN se cree libremente
    # o usar una API KEY secreta en el header.
    return AuthUsecase().register_user(
        email=data.email,
        password=data.password,
        role=data.role,
        full_name=data.full_name,
    )
