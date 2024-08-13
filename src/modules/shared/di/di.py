from src.config.app import EMAIL_SMTP
from src.modules.user.repositories import UserRepository
from src.modules.auth.repositories import PasswordRepository
from src.modules.auth.repositories import VerificationTokenRepository
from src.modules.user.services import UserService
from src.modules.auth.services import AuthService
from src.modules.auth.services import PasswordService
from src.modules.shared.sql import DatabaseManager
from src.modules.shared.services import EmailService
from src.modules.auth.services import VerificationTokenService

session = DatabaseManager().get_session()
user_repository = UserRepository(session)
password_repository = PasswordRepository(session)
verification_token_repository = VerificationTokenRepository(session)
user_service = UserService(user_repository)
password_service = PasswordService(password_repository)
verification_token_service = VerificationTokenService(
    verification_token_repository)
email_service = EmailService(**EMAIL_SMTP)
auth_service = AuthService(user_service, email_service,
                           password_service, verification_token_service)
