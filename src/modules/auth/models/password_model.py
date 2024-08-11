from sqlalchemy import Column, String, Integer, ForeignKey
from src.modules.shared.sql import BaseModel


class PasswordModel(BaseModel):
    __tablename__ = 'passwords'

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    password = Column(String(120), nullable=False)
    salt = Column(String(120), nullable=False)

    def __repr__(self):
        return f"<Password(id={self.id}, user_id={self.user_id})>"
