from fastapi import HTTPException, Depends, status
from dddpy.auth.usecase.auth_cmd_schema import UserRole
from dddpy.auth.usecase.auth_usecase import get_current_user


class AuthChecker:
    def __init__(self, allowed_roles: list[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, user_data: dict = Depends(get_current_user)):
        # Validamos si el rol del usuario está en la lista permitida
        if user_data.get("role") not in [role.value for role in self.allowed_roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permisos insuficientes. Se requiere uno de: {[r.value for r in self.allowed_roles]}",
            )
        return user_data
