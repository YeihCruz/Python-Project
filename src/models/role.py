from sqlalchemy import Column, Integer, String
from src.database.connection import Base


class Role(Base):
    """Modelo Python equivalente a models.Role.java"""
    __tablename__ = "role"

    role_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)

    def __repr__(self):
        return self.name
