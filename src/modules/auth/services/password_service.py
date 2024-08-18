import bcrypt
from typing import Optional
from sqlalchemy.orm import Session
from src.modules.shared.services import logger
from src.modules.auth.models import PasswordModel
from src.modules.auth.repositories import PasswordRepository


class PasswordService:
    def __init__(self, password_repository: PasswordRepository):
        self.password_repository = password_repository

    def get_password(self, user_id: str) -> PasswordModel:
        return self.password_repository.get_by_props({"user_id": user_id})

    def create(self, user_id: str, password: str, session: Optional[Session] = None):
        try:
            existing_password = self.get_password(user_id)
            if existing_password:
                raise Exception("Password already exists")
            logger.info(f"Creating password for user {user_id}")
            salt = bcrypt.gensalt().decode()
            logger.info("Salt created")
            hash = bcrypt.hashpw(
                password.encode(), salt.encode()).decode()
            logger.info("Password hashed")
            data = {
                "user_id": user_id,
                "salt": salt,
                "hash": hash,
            }
            logger.info("Password entity data created")
            return self.password_repository.set_session(session).create(data)
        except Exception as e:
            logger.error(f"Error creating password for user {user_id}: {e}")
            raise e

    def update(self, user_id: str, new_password: str, session: Optional[Session] = None):
        try:
            logger.info(f"Updating password for user {user_id}")
            password = self.get_password(user_id)
            if not password:
                raise Exception("Password not found")
            salt = password.salt.encode()
            logger.info("Salt encoded")
            hash = bcrypt.hashpw(
                new_password.encode(), salt
            ).decode()
            logger.info("Password hashed")
            data = {
                "hash": hash,
            }
            return self.password_repository.set_session(session).update_by_props({"user_id": user_id}, data)
        except Exception as e:
            logger.error(f"Error updating password for user {user_id}: {e}")
            raise e

    def verify(self, user_id: str, password_str: str) -> bool:
        logger.info(f"Verifying password for user {user_id}")
        password = self.get_password(user_id)
        if not password:
            logger.error(f"Password not found for user {user_id}")
            return False
        logger.info(f"Password found for user {user_id}")
        verified = bcrypt.checkpw(
            password_str.encode(), password.hash.encode())
        logger.info(f"Password verified for user {user_id}: {verified}")
        return verified
