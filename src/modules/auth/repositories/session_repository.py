from typing import Any, Dict
from sqlalchemy.orm import Session
from src.modules.auth.models import SessionModel
from src.modules.shared.sql import BaseRepository


class SessionRepository(BaseRepository[SessionModel]):
    def __init__(self, session: Session):
        super().__init__(session, SessionModel)

    def to_dict(self, entity: SessionModel) -> Dict[str, Any]:
        return {
            "user_id": entity.user_id,
            "token": entity.token,
            "expires_at": entity.expires_at,
        }
