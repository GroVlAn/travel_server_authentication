from passlib.context import CryptContext

from auth.abstract_classes import ABCPasswordHandler


class PasswordHandler(ABCPasswordHandler):

    def __init__(
            self,
            secret: str,
            algorithm: str
    ):
        self.secret = secret
        self.algorithm = algorithm
        self.pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    async def encode(self, password):
        return self.pwd_context.hash(password)

    async def verify(self, password: str, hashed_password: str):
        return self.pwd_context.verify(password, hashed_password)
