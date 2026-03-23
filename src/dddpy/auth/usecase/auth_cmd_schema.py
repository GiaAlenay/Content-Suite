import re
from pydantic import BaseModel, Field, EmailStr, field_validator
from pydantic import EmailStr
from enum import Enum


class UserRole(str, Enum):
    CREATOR = "CREATOR"
    APPROVER = "APPROVER"
    ADMIN = "ADMIN"


class RegisterSchema(BaseModel):
    email: EmailStr = Field(..., max_length=100)
    password: str = Field(..., min_length=8, max_length=255)
    role: UserRole
    full_name: str = Field(..., max_length=100)

    @field_validator("password")
    @classmethod
    def validate_password_complexity(cls, v: str) -> str:
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError("Password must contain at least one special character")
        return v


class LoginSchema(BaseModel):
    email: EmailStr = Field(..., max_length=100)
    password: str = Field(..., min_length=8, max_length=255)
