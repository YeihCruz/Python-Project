from sqlalchemy import Column, Integer, String
from src.database.connection import Base


class ClaimType(Base):
    """Modelo Python equivalente a models.ClaimType.java"""
    __tablename__ = "claim_type"

    claim_type_id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(50), nullable=False, unique=True)

    def __repr__(self):
        return self.description
