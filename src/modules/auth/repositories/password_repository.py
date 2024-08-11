from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from ..models import PasswordModel
from src.modules.shared.sql import BaseRepository


class PasswordRepository(BaseRepository[PasswordModel]):
    def __init__(self, session: Session):
        super().__init__(session, PasswordModel)

    def to_dict(self, entity: PasswordModel) -> Dict[str, Any]:
        return {
            'id': entity.id,
            'user_id': entity.user_id,
        }

    def find_by_user_id(self, user_id: str) -> Optional[PasswordModel]:
        return self.session.query(PasswordModel).filter(PasswordModel.user_id == user_id).first()
