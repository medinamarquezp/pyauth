from src.modules.shared.sql import BaseModel
from sqlalchemy import Column, String, ForeignKey


class PasswordModel(BaseModel):
    __tablename__ = 'passwords'

    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    hash = Column(String(120), nullable=False)
    salt = Column(String(120), nullable=False)

    def __repr__(self):
        return f"<Password(id={self.id}, user_id={self.user_id})>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "hash": self.hash,
            "salt": self.salt
        }
