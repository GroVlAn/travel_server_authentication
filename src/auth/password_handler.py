import re

from fastapi import HTTPException
from passlib.context import CryptContext
from starlette import status

from auth.abstract_classes import ABCPasswordHandler
from schemas.request import ExceptionResponse, ExceptionDetails


class PasswordHandler(ABCPasswordHandler):

    def __init__(
            self,
            secret: str,
            algorithm: str
    ):
        self.secret = secret
        self.algorithm = algorithm
        self.pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
        self.validation_rules = (
            r'.*[a-z]',
            r'.*[A-Z]',
            r'.*\d',
            r'.*[^\w\s]'
        )

    async def encode(self, password):
        return self.pwd_context.hash(password)

    async def verify(self, password: str, hashed_password: str):
        return self.pwd_context.verify(password, hashed_password)

    def validate_password(self, password: str):
        errors = []
        print(password)
        print(re.match(self.validation_rules[0], password))
        if not re.match(self.validation_rules[0], password):
            errors.append('Пароль должен содержать латинские символы в нижнем регистре')

        if not re.match(self.validation_rules[1], password):
            errors.append('Пароль должен содержать латинские символы в верхнем регистре')

        if not re.match(self.validation_rules[2], password):
            errors.append('Пароль должен содержать цифры')

        if not re.match(self.validation_rules[3], password):
            errors.append('Пароль должен содержать спец символы')

        if len(errors) > 0:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=ExceptionResponse(
                status='error',
                details=ExceptionDetails(
                    field='password',
                    errors=errors
                )
            ).model_dump())
