from typing import Optional
from sqlalchemy.orm import Session

from ..models import PasswordModel
from src.modules.shared.sql import BaseRepository

class PasswordRepository(BaseRepository[PasswordModel]):
    def __init__(self, session: Session):
        super().__init__(session, PasswordModel)

    def find_by_user_id(self, user_id: str) -> Optional[PasswordModel]:
        return self.get_by_props({"user_id": user_id})
