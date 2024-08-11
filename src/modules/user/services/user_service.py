from src.modules.shared.services import logger
from src.modules.user.models import UserModel
from src.modules.user.repositories import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create(self, data: dict) -> UserModel:
        try:
            logger.info("Creating user")
            return self.user_repository.create(data)
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise e
