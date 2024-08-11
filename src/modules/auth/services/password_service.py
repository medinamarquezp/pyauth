import bcrypt
from src.modules.auth.repositories import PasswordRepository


class PasswordService:
    def __init__(self, password_repository: PasswordRepository):
        self.password_repository = password_repository

    def create(self, user_id: str, password: str):
        salt = bcrypt.gensalt().decode()
        hashed_password = bcrypt.hashpw(
            password.encode(), salt.encode()).decode()
        data = {
            "user_id": user_id,
            "salt": salt,
            "password": hashed_password,
        }
        return self.password_repository.create(data)
