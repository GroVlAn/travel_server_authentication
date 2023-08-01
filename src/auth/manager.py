from datetime import timedelta, datetime
from typing import Optional

from fastapi import HTTPException
from jose import jwt
from starlette import status

from auth.abstract_classes import ABCUserDB, ABCManager
from auth.exceptions import UserExist
from auth.password_handler import PasswordHandler
from auth.shemas import UserRead, UserCreate
from config import SECRET, ALGORITHM
from schemas.request import MainResponse


class Manager(ABCManager):
    """
    Manager of user db
    """

    _SECRET_KEY = SECRET
    _ALGORITHM = ALGORITHM

    def __init__(
            self,
            user_db: ABCUserDB
    ):
        self.user_db = user_db
        self.password_handler = PasswordHandler(
            secret=self._SECRET_KEY,
            algorithm=self._ALGORITHM
        )

    async def read(
            self,
            username: Optional[str] = None,
    ) -> UserRead:

        if '@' in username:
            return await self.user_db.get_by_email(email=username)
        else:
            return await self.user_db.get_by_username(username=username)

    async def create(
            self,
            user_created: UserCreate
    ) -> dict:
        """
        Create user
        :param user_created: UserCreate - schema of use
        :return:
        """
        existed_user_by_email = await self.user_db.exist(email=user_created.email)
        existed_user_by_username = await self.user_db.exist(username=user_created.username)

        self.password_handler.validate_password(user_created.password)

        if existed_user_by_email or existed_user_by_username:
            raise UserExist('User exist')

        user_dict = {
            **user_created.refactor(
                exclude={
                    'is_active',
                    'password',
                    'is_verified',
                    'is_superuser',
                }
            ),
        }

        password = await self.password_handler.encode(user_created.password)

        user_dict['hashed_password'] = password
        user_dict['role_id'] = 1

        created_user = await self.user_db.create(user_dict)

        return user_dict

    async def authenticate_user(self, username: str, user_password: str):
        try:
            if '@' in username:
                user = await self.user_db.get_by_email(email=username)
            else:
                user = await self.user_db.get_by_username(username=username)
        except IndexError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=MainResponse(
                status='error',
                data=None,
                details='Пользователь не найден'
            ).model_dump())

        if user is None:
            return False
        if not await self.password_handler.verify(password=user_password, hashed_password=user.hashed_password):
            return False

        return True

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self._SECRET_KEY, algorithm=self._ALGORITHM)
        return encoded_jwt
