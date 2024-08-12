from typing import Any, Dict
from sqlalchemy.orm import Session
from src.modules.shared.sql import BaseRepository
from src.modules.auth.models import VerificationTokenModel


class VerificationTokenRepository(BaseRepository[VerificationTokenModel]):
    def __init__(self, session: Session):
        super().__init__(session, VerificationTokenModel)

    def to_dict(self, entity: VerificationTokenModel) -> Dict[str, Any]:
        return {
            "token": entity.token,
            "user_id": entity.user_id,
            "expires_at": entity.expires_at,
        }
