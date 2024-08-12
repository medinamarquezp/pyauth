import secrets
from datetime import datetime, timedelta

from src.modules.auth.models import VerificationTokenModel
from src.modules.auth.repositories import VerificationTokenRepository


class VerificationTokenService:
    def __init__(self, repository: VerificationTokenRepository):
        self.repository = repository

    def create(self, user_id: str) -> VerificationTokenModel:
        data = {
            "user_id": user_id,
            "token": secrets.token_urlsafe(24),
            "expires_at": datetime.now() + timedelta(days=1),
        }
        return self.repository.create(data)

    def get_by_token(self, token: str) -> VerificationTokenModel:
        return self.repository.get_by_props({"token": token})

    def is_expired(self, token: str) -> bool:
        verification_token = self.get_by_token(token)
        if not verification_token:
            return True
        return verification_token.expires_at.timestamp() < datetime.now().timestamp()

    def delete(self, token: str) -> None:
        return self.repository.delete_by_properties({"token": token})
