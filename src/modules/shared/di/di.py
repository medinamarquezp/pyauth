from src.modules.user.repositories import UserRepository
from src.modules.auth.repositories import PasswordRepository
from src.modules.user.services import UserService
from src.modules.auth.services import AuthService
from src.modules.auth.services import PasswordService
from src.modules.shared.sql import DatabaseManager

session = DatabaseManager().get_session()
user_repository = UserRepository(session)
password_repository = PasswordRepository(session)
user_service = UserService(user_repository)
password_service = PasswordService(password_repository)
auth_service = AuthService(user_service, password_service)
