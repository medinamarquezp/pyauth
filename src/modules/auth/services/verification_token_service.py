import secrets
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from src.modules.shared.services import logger
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

    def verify_token(self, token_str: str, session: Optional[Session] = None):
        token = self.get_by_token(token_str)
        response = {"user_id": None, "verified": False}
        if not token:
            logger.error(f"Verification token {token_str} not found")
            return response
        response["user_id"] = str(token.user_id)
        if self.is_expired(token):
            logger.error(f"Verification token {token_str} is expired")
            return response
        if self.is_verified(token):
            logger.error(f"Verification token {token_str} is already verified")
            return response
        self.repository.set_session(session).update(str(token.id), {
            "verified_at": datetime.now()
        })
        logger.info(f"Verification token {token_str} has been verified")
        response["verified"] = True
        return response
