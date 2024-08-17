from enum import Enum as PyEnum
from src.modules.shared.sql import BaseModel
from sqlalchemy import Column, DateTime, String, Enum, ForeignKey

class TokenType(PyEnum):
    SIGNUP = "SIGNUP"
    FORGOT = "FORGOT"

class VerificationTokenModel(BaseModel):
    __tablename__ = "verification_tokens"

    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    token = Column(String, nullable=False)
    verified_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=False)
    type = Column(Enum(TokenType), nullable=False)
    
    def __repr__(self):
        return f"<VerificationTokenModel(user_id={self.user_id}, type={self.type}, token={self.token}, expires_at={self.expires_at})>"
