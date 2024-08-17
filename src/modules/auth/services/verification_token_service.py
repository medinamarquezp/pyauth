import secrets
from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from src.modules.shared.services import logger
from src.modules.auth.models import VerificationTokenModel, TokenType
from src.modules.auth.repositories import VerificationTokenRepository


class VerificationTokenService:
    def __init__(self, repository: VerificationTokenRepository):
        self.repository = repository

    def create(self, user_id: str, type: TokenType, session: Optional[Session] = None) -> VerificationTokenModel:
        token = self.get_by_user_id(user_id, type)
        if token and not token.is_expired:
            return token
        data = {
            "user_id": user_id,
            "token": secrets.token_urlsafe(24),
            "expires_at": datetime.now() + timedelta(days=1),
            "type": type
        }
        return self.repository.set_session(session).create(data)

    def get_by_token(self, token: str) -> VerificationTokenModel:
        return self.repository.get_by_props({"token": token})
    
    def get_by_user_id(self, user_id: str, type: TokenType) -> VerificationTokenModel:
        return self.repository.get_by_props({"user_id": user_id, "type": type})

    def verify_token(self, token_str: str, session: Optional[Session] = None):
        token = self.get_by_token(token_str)
        response = {"user_id": None, "verified": False}
        if not token:
            logger.error(f"Verification token {token_str} not found")
            return response
        response["user_id"] = str(token.user_id)
        if token.is_expired:
            logger.error(f"Verification token {token_str} is expired")
            return response
        if token.is_verified:
            logger.error(f"Verification token {token_str} is already verified")
            return response
        self.repository.set_session(session).update(str(token.id), {
            "verified_at": datetime.now()
        })
        logger.info(f"Verification token {token_str} has been verified")
        response["verified"] = True
        return response
