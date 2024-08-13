from typing import Optional
from sqlalchemy.orm import Session

from src.modules.shared.services import logger
from src.modules.user.models import UserModel
from src.modules.user.repositories import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create(self, data: dict, session: Optional[Session] = None) -> UserModel:
        try:
            logger.info("Creating user")
            return self.user_repository.set_session(session).create(data)
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise e

    def get_by_email(self, email: str) -> UserModel:
        try:
            logger.info(f"Getting user by email: {email}")
            return self.user_repository.find_by_email(email)
        except Exception as e:
            logger.error(f"Error getting user by email: {e}")
            raise e
