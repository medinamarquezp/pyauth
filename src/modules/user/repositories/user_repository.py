from typing import Optional
from sqlalchemy.orm import Session

from ..models import UserModel
from src.modules.shared.sql import BaseRepository

class UserRepository(BaseRepository[UserModel]):
    def __init__(self, session: Session):
        super().__init__(session, UserModel)

    def find_by_email(self, email: str) -> Optional[UserModel]:
        return self.get_by_props({"email": email})
