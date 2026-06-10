from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.database.connection import Base


class User(Base):
    """Modelo Python equivalente a models.User.java"""
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey("role.role_id"), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    active = Column(Boolean, nullable=False, default=True)

    role = relationship("Role")

    def __repr__(self):
        return self.username
