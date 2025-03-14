from enum import Enum as PyEnum
from sqlalchemy import Column, String, Enum, DateTime
from src.modules.shared.sql import BaseModel

class UserRole(PyEnum):
    ADMIN = "ADMIN"
    USER = "USER"
    
class UserStatus(PyEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    PENDING_ACTIVATION = "PENDING_ACTIVATION"

class UserModel(BaseModel):
    __tablename__ = 'users'

    name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    email = Column(String(120), unique=True, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER)
    status = Column(Enum(UserStatus), default=UserStatus.PENDING_ACTIVATION)
    last_login = Column(DateTime(timezone=True), nullable=True)

    @property
    def full_name(self):
        return f"{self.name} {self.last_name}"

    @property
    def role_value(self):
        return self.role.value

    @property
    def status_value(self):
        return self.status.value

    @property
    def is_active(self):
        return self.status_value == UserStatus.ACTIVE.value

    @property
    def is_inactive(self):
        return self.status_value == UserStatus.INACTIVE.value

    @property
    def is_admin(self):
        return self.role_value == UserRole.ADMIN.value

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', email='{self.email}', status='{self.status_value}')>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "email": self.email,
            "role": self.role_value,
            "status": self.status_value,
            "last_login": self.last_login
        }
