from sqlalchemy.orm import Session

from ..models import PasswordModel
from src.modules.shared.sql import BaseRepository

class PasswordRepository(BaseRepository[PasswordModel]):
    def __init__(self, session: Session):
        super().__init__(session, PasswordModel)
