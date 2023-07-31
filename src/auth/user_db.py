from typing import Any

from fastapi import Depends, HTTPException
from sqlalchemy import Table, insert, exists, select, Select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.abstract_classes import ABCUserDB
from auth.models import User
from auth.shemas import UserRead, UserCreate
from database import get_async_session


class UserDB(ABCUserDB):
    """
    Class authentication user
    - model: Table (model user db)
    - session: AsyncSession (global async session db)
    """

    def __init__(
            self,
            model: UserCreate,
            session: AsyncSession
    ):
        """

        :param model: Table (model user db)
        """
        self.model = model
        self.session = session

    async def create(
            self,
            user_dict: dict
    ) -> None:
        """

        :param user_dict: User (schema user)
        :return: boot or HTTPException (status created
        """
        stmt = insert(User).values(**user_dict)
        result = await self.session.execute(stmt)
        await self.session.commit()

    async def update(
            self,
            user_created: UserCreate
    ) -> bool:
        pass

    async def remove(
            self,
            user_id: int
    ) -> bool:
        pass

    async def exist(
            self,
            user_id: int = None,
            email: str = None,
            username: str = None
    ) -> bool:
        if not user_id and not email and not username:
            raise Exception('user_id or email or username must be not empty')

        if user_id:
            query = select(User).where(User.c.id == user_id)
            result = await self.session.execute(query)

            return result.scalar()

        if email:
            query = select(User).where(User.c.email == email)
            print(self.session)
            result = await self.session.execute(query)

            return result.scalar()

        if username:
            query = select(User).where(User.c.username == username)
            result = await self.session.execute(query)

            return result.scalar()

    async def _get_user_by_query(
            self,
            query: Select[Any]
    ) -> UserRead:
        result = await self.session.execute(query)
        user_result = result.all()[0]
        print(user_result)
        user = UserRead(
            id=user_result[0],
            username=user_result[1],
            email=user_result[2],
            hashed_password=user_result[3],
            first_name=user_result[4],
            last_name=user_result[5],
            middle_name=user_result[6],
            role_id=user_result[12],
        )

        return user

    async def get_by_id(
            self,
            user_id: int
    ) -> UserRead:
        query = select(User).where(User.c.id == user_id)
        return await self._get_user_by_query(query)

    async def get_by_username(
            self,
            username: str
    ) -> UserRead:
        query = select(User).where(User.c.username == username)
        return await self._get_user_by_query(query)

    async def get_by_email(
            self,
            email: str
    ) -> UserRead:
        query = select(User).where(User.c.email == email)
        return await self._get_user_by_query(query)
