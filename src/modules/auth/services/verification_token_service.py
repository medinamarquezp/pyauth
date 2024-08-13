import secrets
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from src.modules.auth.models import VerificationTokenModel
from src.modules.auth.repositories import VerificationTokenRepository


class VerificationTokenService:
    def __init__(self, repository: VerificationTokenRepository):
        self.repository = repository

    def create(self, user_id: str, session: Optional[Session] = None) -> VerificationTokenModel:
        data = {
            "user_id": user_id,
            "token": secrets.token_urlsafe(24),
            "expires_at": datetime.now() + timedelta(days=1)
        }
        return self.repository.set_session(session).create(data)

    def get_by_token(self, token: str) -> VerificationTokenModel:
        return self.repository.get_by_props({"token": token})

    def is_expired(self, verification_token: VerificationTokenModel) -> bool:
        return verification_token.expires_at.timestamp() < datetime.now().timestamp()

    def is_verified(self, verification_token: VerificationTokenModel) -> bool:
        return verification_token.verified_at is not None

    def verify_token(self, token: str) -> bool:
        vtoken = self.get_by_token(token)
        if not vtoken:
            return False
        if self.is_expired(vtoken):
            return False
        if self.is_verified(vtoken):
            return False
        id = str(vtoken.id)
        data = {
            "verified_at": datetime.now()
        }
        self.repository.update(id, data)
        return True
