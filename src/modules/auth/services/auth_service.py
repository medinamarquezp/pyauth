import jsonschema
from jsonschema import validate

from ..schemas import signup_schema
from .password_service import PasswordService
from src.modules.shared.services import logger
from src.modules.user.services import UserService
from src.modules.shared.sql import DatabaseManager


class AuthService:
    def __init__(
        self,
        user_service: UserService,
        password_service: PasswordService
    ):
        self.user_service = user_service
        self.password_service = password_service

    def signup(self, data: dict):
        session = DatabaseManager().get_session()
        try:
            session.begin()
            validate(instance=data, schema=signup_schema)
            existing_user = self.user_service.get_by_email(data["email"])
            if existing_user:
                raise ValueError("User already exists")
            logger.info(f"Signing up user: {data['email']}")
            password = data.pop("password", None)
            logger.info("Password extracted from incoming data")
            user = self.user_service.create(data)
            logger.info(f"User created: {user.id}")
            created_password = self.password_service.create(
                str(user.id), password)
            logger.info(f"Password created: {created_password.id}")
            session.commit()
            return user
        except jsonschema.ValidationError as err:
            logger.error(f"Error validating signup data: {err}")
            session.rollback()
            raise err
        except Exception as err:
            logger.error(f"Error signing up: {err}")
            session.rollback()
            raise err
        finally:
            session.close()
