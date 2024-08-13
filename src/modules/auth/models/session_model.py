from src.modules.shared.sql import BaseModel
from sqlalchemy import Column, DateTime, String, ForeignKey


class SessionModel(BaseModel):
    __tablename__ = "sessions"

    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    session_id = Column(String(36), nullable=False)
    expires_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<SessionModel(user_id={self.user_id}, session_id={self.session_id}, expires_at={self.expires_at})>"
