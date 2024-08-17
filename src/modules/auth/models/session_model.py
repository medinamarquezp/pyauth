from src.modules.shared.sql import BaseModel
from sqlalchemy import Column, DateTime, String, ForeignKey


class SessionModel(BaseModel):
    __tablename__ = "sessions"

    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    token = Column(String(36), nullable=False)
    expires_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<SessionModel(user_id={self.user_id}, token={self.token}, expires_at={self.expires_at})>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "token": self.token,
            "expires_at": self.expires_at
        }
