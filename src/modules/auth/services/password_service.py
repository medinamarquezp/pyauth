import bcrypt
from src.modules.shared.services import logger
from src.modules.auth.repositories import PasswordRepository


class PasswordService:
    def __init__(self, password_repository: PasswordRepository):
        self.password_repository = password_repository

    def create(self, user_id: str, password: str):
        try:
            logger.info(f"Creating password for user {user_id}")
            salt = bcrypt.gensalt().decode()
            logger.info("Salt created")
            hashed_password = bcrypt.hashpw(
                password.encode(), salt.encode()).decode()
            logger.info("Password hashed")
            data = {
                "user_id": user_id,
                "salt": salt,
                "password": hashed_password,
            }
            logger.info("Password entity data created")
            return self.password_repository.create(data)
        except Exception as e:
            logger.error(f"Error creating password for user {user_id}: {e}")
            raise e
