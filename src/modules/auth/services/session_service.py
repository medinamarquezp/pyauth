import secrets
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from src.modules.shared.services import logger
from src.modules.auth.models import SessionModel
from src.modules.auth.repositories import SessionRepository


class SessionService:
    def __init__(self, repository: SessionRepository):
        self.repository = repository

    def get_user_session(self, user_id: str) -> SessionModel | None:
        session = self.repository.get_by_props({"user_id": user_id })
        if not session:
            return None
        if self.check_expired(session):
            return None
        return session

    def create(self, user_id: str, session: Optional[Session] = None) -> SessionModel:
        existing_session = self.get_user_session(user_id)
        if existing_session:
            logger.info(f"Existing session: {existing_session.id}")
            return existing_session
        data = {
            "user_id": user_id,
            "token": secrets.token_urlsafe(32),
            "expires_at": datetime.now() + timedelta(days=1)
        }
        logger.info(f"Creating session for user {user_id}")
        return self.repository.set_session(session).create(data)

    def is_session_expired(self, token: str) -> bool:
        session = self.repository.get_by_props({ "token": token })
        if not session:
            return True
        return self.check_expired(session)

    def check_expired(self, session: SessionModel) -> bool:
        return session.expires_at.timestamp() < datetime.now().timestamp()
    
    def expire_session(self, token: str) -> bool:
        session_expired = self.repository.update_by_props({ "token": token }, { "expires_at": datetime.now() })
        if not session_expired:
            return False
        logger.info(f"Expired session of user {session_expired.user_id}")
        return True
