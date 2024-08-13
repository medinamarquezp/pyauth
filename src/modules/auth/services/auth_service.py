import jsonschema
from jsonschema import validate
from sqlalchemy.orm import Session

from src.config.app import APP
from ..schemas import signup_schema
from .password_service import PasswordService
from src.modules.user.models import UserModel
from src.modules.shared.services import logger
from src.modules.user.services import UserService
from src.modules.shared.sql import DatabaseManager
from src.modules.shared.services import EmailService
from src.modules.shared.translations import get_email_contents
from src.modules.auth.services.verification_token_service import VerificationTokenService


class AuthService:
    def __init__(
        self,
        user_service: UserService,
        email_service: EmailService,
        password_service: PasswordService,
        verification_token_service: VerificationTokenService,
    ):
        self.user_service = user_service
        self.email_service = email_service
        self.password_service = password_service
        self.verification_token_service = verification_token_service

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
            user = self.user_service.create(data, session)
            logger.info(f"User created: {user.id}")
            created_password = self.password_service.create(
                str(user.id), password, session)
            logger.info(f"Password created: {created_password.id}")
            self.send_signup_email(user, session)
            logger.info(f"Signup email sent to: {user.email}")
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

    def send_signup_email(self, user: UserModel, session: Session, language="es"):
        token = self.verification_token_service.create(
            str(user.id), session).token
        email_contents = get_email_contents(language, "signup")
        subject = email_contents["subject"]
        verification_link = f"{APP['FRONTEND_URL']
                               }/signup/activate?token={token}"
        content = email_contents["content"].replace(
            "{{verification_link}}", verification_link)
        self.email_service.send_email(user.email, subject, content)
