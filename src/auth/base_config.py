from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.manager import Manager
from auth.models import User
from auth.user_db import UserDB
from database import get_async_session


def create_manager(session: AsyncSession = Depends(get_async_session)):
    user_db = UserDB(User, session)
    manager = Manager(user_db=user_db)
    return manager
