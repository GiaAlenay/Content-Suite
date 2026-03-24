from fastapi import HTTPException, Depends, status
from dddpy.auth.usecase.auth_cmd_schema import UserRole
from dddpy.auth.usecase.auth_usecase import get_current_user

from dddpy.auth.context import current_user_ctx


class AuthChecker:
    def __init__(self, allowed_roles: list[UserRole] = None):
        self.allowed_roles = allowed_roles

    def __call__(self, user_data: dict = Depends(get_current_user)):

        current_user_ctx.set(user_data)

        user_role = user_data.get("role")

        if user_role == UserRole.ADMIN.value:
            return user_data

        if not self.allowed_roles:
            return user_data

        allowed_values = [role.value for role in self.allowed_roles]
        if user_role not in allowed_values:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permisos insuficientes. Se requiere uno de: {allowed_values}",
            )

        return user_data
