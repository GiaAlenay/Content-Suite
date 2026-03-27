import jwt  # PyJWT
from fastapi import status, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
from dotenv import load_dotenv
from dddpy.shared.supabase.supabase_manager import supabase

load_dotenv()
from dddpy.shared.logging.logging import Logger

logging = Logger("AuthUsecase")


SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")
ALGORITHM = "HS256"

security = HTTPBearer()


class AuthUsecase:
    def __init__(self):
        logging.info("__init__")
        self.supabase = supabase

    def register_user(self, email: str, password: str, role: str, full_name: str):
        try:

            response = self.supabase.auth.admin.create_user(
                {
                    "email": email,
                    "password": password,
                    "user_metadata": {"full_name": full_name},
                    "app_metadata": {"role": role},
                    "email_confirm": True,
                }
            )

            logging.info(f"User created successfully: {email} with role {role}")

            return {
                "id": response.user.id,
                "email": response.user.email,
                "role": role,
                "full_name": full_name,
            }

        except Exception as e:
            logging.error(f"Error registering user: {str(e)}")
            raise HTTPException(
                status_code=400, detail=f"Error al registrar usuario: {str(e)}"
            )

    async def get_current_user(
        self,
        credentials: HTTPAuthorizationCredentials = Security(security),
    ):

        token = credentials.credentials

        try:
            user_response = self.supabase.auth.get_user(token)

            if not user_response or not user_response.user:
                raise HTTPException(
                    status_code=401, detail="Token inválido o usuario no encontrado"
                )

            user = user_response.user

            role = user.app_metadata.get("role")

            if not role:
                logging.error(
                    f"Usuario {user.email} intentó entrar sin rol en app_metadata"
                )
                raise HTTPException(
                    status_code=403, detail="Usuario autenticado pero sin rol asignado"
                )

            return {"id": user.id, "role": role, "email": user.email}

        except Exception as e:
            logging.error(f"Error de autenticación: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token no válido o expirado",
            )

    def login(self, email: str, password: str):
        """
        Autentica al usuario y devuelve el Access Token (JWT).
        """
        try:
            response = self.supabase.auth.sign_in_with_password(
                {"email": email, "password": password}
            )
            # El access_token es el que usarás en el Header Authorization: Bearer ...
            return {
                "access_token": response.session.access_token,
                "refresh_token": response.session.refresh_token,
                "user": response.user,
            }
        except Exception as e:
            logging.error(f"Error en login: {str(e)}")
            raise HTTPException(status_code=401, detail="Credenciales inválidas")

    def logout(self, token: str):
        """
        Invalida la sesión en Supabase.
        """
        try:
            # Supabase maneja la invalidación del lado del servidor
            self.supabase.auth.sign_out()
            return {"message": "Sesión cerrada correctamente"}
        except Exception as e:
            raise HTTPException(status_code=400, detail="Error al cerrar sesión")


_auth_service = AuthUsecase()


get_current_user = _auth_service.get_current_user
