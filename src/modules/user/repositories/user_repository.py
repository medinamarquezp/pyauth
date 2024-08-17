from sqlalchemy.orm import Session
from typing import Dict, Any, Optional

from ..models import UserModel
from src.modules.shared.sql import BaseRepository


class UserRepository(BaseRepository[UserModel]):
    def __init__(self, session: Session):
        super().__init__(session, UserModel)

    def to_dict(self, entity: UserModel) -> Dict[str, Any]:
        return {
            'id': entity.id,
            'name': entity.name,
            'last_name': entity.last_name,
            'email': entity.email,
            'role': entity.role_value,
            'status': entity.status_value,
            'language': entity.language,
            'last_login': entity.last_login,
            'created_at': entity.created_at,
            'updated_at': entity.updated_at,
        }

    def find_by_email(self, email: str) -> Optional[UserModel]:
        return self.get_by_props({"email": email})
