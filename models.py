import re
from typing import Literal
from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    field_validator
)


class BaseUser(BaseModel):
    first_name: str = Field(description="Имя пользователя")
    last_name: str = Field(description="Фамилия пользователя")
    email: EmailStr = Field(description="E-mail пользователя")

    @field_validator("first_name", "last_name", mode="before")
    def capitalize_name(cls, value: str) -> str:
        return value.capitalize() if value else value


class User(BaseUser):
    password: str = Field(
        min_length=8, exclude=True,
        description="""
            Пароль должен содержать минимум 8 символов, 1 цифру и 1 спецсимвол!
        """
    )
    age: int = Field(
        ge=18, le=120,
        description="Возраст должен быть от 18 до 120 лет!"
    )

    @field_validator("password", mode="before")
    def validate_password(cls, value):
        has_digit = bool(re.search(r"\d", value))
        has_special = bool(re.search(r"[^\w\s]", value))
        if not (has_digit and has_special):
            raise ValueError(
                "Пароль должен содержать хотя бы 1 цифру и 1 спецсимвол!"
            )
        return value


class AdminUser(User):
    role: Literal["admin", "superadmin"] = Field(description="Уровень доступа")

    def has_permission(self, permission: str) -> bool:
        permissions_map = {
            "admin": {"read", "write", "delete"},
            "superadmin": {
                "read", "write", "delete", "manage_users", "manage_admins"
            },
        }
        return permission in permissions_map.get(self.role, set())
