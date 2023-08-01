import re
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Json, EmailStr, field_validator


class Role(BaseModel):
    id: int
    name: str
    permission: Json[List[str]]
    created_at: Optional[datetime]
    modified_at: Optional[datetime]


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    is_active: bool = False
    is_verified: bool = False
    is_superuser: bool = False
    role_id: Optional[int] = 1

    def refactor(
            self,
            exclude: Optional[set] = None
    ):
        user_create = self.model_dump()

        if exclude is not None:
            for field in tuple(exclude):
                user_create.pop(field)

        return user_create


class UserRead(BaseModel):
    id: int
    username: str
    email: str
    hashed_password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    role_id: int
