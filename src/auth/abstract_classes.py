from abc import ABC, abstractmethod
from typing import Optional

from auth.models import User
from auth.shemas import UserCreate, UserRead


class ABCUserDB(ABC):

    @abstractmethod
    async def create(
            self,
            user_dict: dict
    ) -> str:
        raise NotImplemented

    @abstractmethod
    async def update(
            self,
            user_created: UserCreate
    ) -> str:
        raise NotImplemented

    @abstractmethod
    async def remove(
            self,
            user_id: int
    ) -> bool:
        raise NotImplemented

    @abstractmethod
    async def get_by_id(
            self,
            user_id: int
    ) -> User:
        raise NotImplemented

    @abstractmethod
    async def get_by_email(
            self,
            email: str
    ) -> User:
        raise NotImplemented

    @abstractmethod
    async def get_by_username(
            self,
            username: str
    ) -> User:
        raise NotImplemented

    @abstractmethod
    async def exist(
            self,
            user_id: int = None,
            email: str = None,
            username: str = None
    ) -> bool:
        raise NotImplemented


class ABCManager(ABC):

    @abstractmethod
    async def create(
            self,
            user_created: UserCreate
    ) -> UserRead:
        raise NotImplemented

    @abstractmethod
    async def read(
            self,
            username: Optional[str] = None
    ) -> UserRead:
        raise NotImplemented


class ABCPasswordHandler(ABC):

    @abstractmethod
    async def encode(self, password):
        raise NotImplemented

    @abstractmethod
    async def verify(self, password: str, hashed_password):
        raise NotImplemented
