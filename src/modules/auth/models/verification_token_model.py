from src.modules.shared.sql import BaseModel
from sqlalchemy import Column, DateTime, String, ForeignKey


class VerificationTokenModel(BaseModel):
    __tablename__ = "verification_tokens"

    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    token = Column(String, nullable=False)
    verified_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<VerificationTokenModel(user_id={self.user_id}, token={self.token}, expires_at={self.expires_at})>"
