from datetime import timedelta

from fastapi import APIRouter, HTTPException, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from auth.base_config import create_manager
from auth.exceptions import UserExist
from auth.manager import Manager
from auth.models import User
from auth.shemas import UserCreate
from auth.user_db import UserDB
from config import ACCESS_TOKEN_EXPIRED_MINUTES
from database import get_async_session
from schemas.request import MainResponse

router = APIRouter(
    prefix=f'/auth/app/v0.0.1/auth',
    tags=['Authentication']
)


@router.post('/token')
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        manager: Manager = Depends(create_manager)
):
    """
    Authenticate user with token
    :param form_data: OAuth2PasswordRequestForm (authenticate form)
    :param manager: Manager (manager of authenticate user)
    :return:
    """
    user = await manager.authenticate_user(
        username=form_data.username,
        user_password=form_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=MainResponse(
                status='error',
                details='Неверный логин или пароль'
            ).model_dump()
        )

    user_read = await manager.read(username=form_data.username)

    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRED_MINUTES))
    access_token = manager.create_access_token(
        data={
            'sub': user_read.id,
            'name': user_read.username,
            'role': user_read.role_id
        },
        expires_delta=access_token_expires
    )
    response = JSONResponse(content={'access_token': access_token})
    response.set_cookie(key='access_token', value=access_token)

    return response


@router.get('/logout', status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response):
    response.delete_cookie(key='access_token')
    return MainResponse(
        status='success',
        details='Logout'
    )


@router.post('/sign-up')
async def token(
        user: UserCreate,
        manager: Manager = Depends(create_manager)
):
    try:
        created_user = await manager.create(user)

        return MainResponse(
            status='success',
            data={
                'username': created_user['username'],
                'email': created_user['email'],
                'first_name': created_user['first_name'],
                'last_name': created_user['last_name'],
                'middle_name': created_user['middle_name']
            },
            details='Создан пользователь'
        ).model_dump()

    except UserExist:
        response = MainResponse(
            status='error',
            details='User exits'
        )
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=response.model_dump())
