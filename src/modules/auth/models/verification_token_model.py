from sqlalchemy import Column, DateTime, String, Integer, ForeignKey
from src.modules.shared.sql import BaseModel


class VerificationTokenModel(BaseModel):
    __tablename__ = "verification_tokens"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<VerificationTokenModel(user_id={self.user_id}, token={self.token}, expires_at={self.expires_at})>"