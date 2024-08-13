from typing import Optional
from sqlalchemy.orm import Session

from src.modules.user.models import UserModel
from src.modules.shared.services import logger
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

    def get_by_id(self, id: str) -> UserModel:
        return self.user_repository.get_by_id(id)

    def get_by_email(self, email: str) -> UserModel:
        return self.user_repository.find_by_email(email)

    def activate(self, id: str, session: Optional[Session] = None) -> bool:
        user = self.user_repository.set_session(
            session).update(id, {"status": "active"})
        if not user:
            logger.error(f"User {id} not found")
            return False
        logger.info(f"User {id} has status {user.status_value}")
        return user.is_active
