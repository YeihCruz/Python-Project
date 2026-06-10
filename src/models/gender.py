from sqlalchemy import Column, Integer, String
from src.database.connection import Base


class Gender(Base):
    """Modelo Python equivalente a models.Gender.java"""
    __tablename__ = "gender"

    gender_id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(20), nullable=False, unique=True)

    def __repr__(self):
        return self.description
