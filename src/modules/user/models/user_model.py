from sqlalchemy import Column, String, Enum, DateTime
from src.modules.shared.sql import BaseModel


class UserModel(BaseModel):
    __tablename__ = 'users'

    name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=True)
    email = Column(String(120), unique=True, nullable=False)
    role = Column(Enum('admin', 'user'), default='user')
    status = Column(Enum('active', 'inactive'), default='active')
    language = Column(Enum('en', 'es'), default='en')
    last_login = Column(DateTime(timezone=True))

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}', status='{self.status}')>"
