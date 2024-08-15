import jsonschema
from jsonschema import validate
from sqlalchemy.orm import Session

from src.config.app import APP
from .password_service import PasswordService
from src.modules.user.models import UserModel
from src.modules.shared.services import logger
from src.modules.auth.models import SessionModel
from src.modules.user.services import UserService
from src.modules.shared.sql import DatabaseManager
from ..schemas import signup_schema, signin_schema
from src.modules.shared.services import EmailService
from src.modules.shared.translations import get_email_contents
from src.modules.auth.services.session_service import SessionService
from src.modules.auth.services.verification_token_service import VerificationTokenService


class AuthService:
    def __init__(
        self,
        user_service: UserService,
        email_service: EmailService,
        session_service: SessionService,
        password_service: PasswordService,
        verification_token_service: VerificationTokenService,
    ):
        self.user_service = user_service
        self.email_service = email_service
        self.session_service = session_service
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
            self._send_signup_email(user, session)
            logger.info(f"Signup email sent to: {user.email}")
            session.commit()
            return True
        except jsonschema.ValidationError as err:
            logger.error(f"Error validating signup data: {err}")
            session.rollback()
            return False
        except Exception as err:
            logger.error(f"Error signing up: {err}")
            session.rollback()
            return False
        finally:
            session.close()

    def verify_signup(self, token_str: str) -> bool:
        session = DatabaseManager().get_session()
        try:
            session.begin()
            token = self.verification_token_service.verify_token(
                token_str, session)
            if not token["verified"]:
                raise ValueError("Token is not verified")
            user_activated = self.user_service.activate(
                token["user_id"], session)
            if not user_activated:
                raise ValueError("User is not activated")
            session.commit()
            return user_activated
        except Exception as err:
            logger.error(f"Error verifying signup: {err}")
            session.rollback()
            return False
        finally:
            session.close()

    def signin(self, data: dict):
        session = DatabaseManager().get_session()
        try:
            session.begin()
            validate(instance=data, schema=signin_schema)
            user = self.user_service.get_by_email(data["email"])
            logger.info(f"User found: {user.id}")
            if not user:
                raise ValueError("User not found")
            if not user.is_active:
                raise ValueError("User is not active")
            user_id = str(user.id)
            if not self.password_service.verify(user_id, data["password"]):
                raise ValueError("Invalid password")
            self.user_service.set_last_login(user_id, session)
            logger.info(f"User last login set to: {user.last_login}")
            auth_session = self.session_service.create(user_id, session)
            logger.info(f"Session created: {auth_session.id}")
            session.commit()
            return self._prepare_signin_response(user, auth_session)
        except Exception as err:
            logger.error(f"Error signing in: {err}")
            session.rollback()
            return False
        finally:
            session.close()

    def _send_signup_email(self, user: UserModel, session: Session, language="es"):
        token = self.verification_token_service.create(
            str(user.id), session).token
        email_contents = get_email_contents(language, "signup")
        subject = email_contents["subject"]
        verification_link = f"{APP['FRONTEND_URL']
                               }/signup/activate?token={token}"
        content = email_contents["content"].replace(
            "{{verification_link}}", verification_link)
        self.email_service.send_email(user.email, subject, content)
        
    def _prepare_signin_response(self, user: UserModel, session: SessionModel):
        response = {
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "role": user.role,
                    "status": user.status,
                },
                "session": {
                    "id": session.id,
                    "token": session.token,
                    "expires_at": session.expires_at.strftime("%Y-%m-%d %H:%M:%S")
            }
        }
        if user.last_login is not None:
            response["user"]["last_login"] = user.last_login.strftime("%Y-%m-%d %H:%M:%S")
        return response
