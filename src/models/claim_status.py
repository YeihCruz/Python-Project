from sqlalchemy import Column, Integer, String
from src.database.connection import Base


class ClaimStatus(Base):
    """Modelo Python equivalente a models.ClaimStatus.java"""
    __tablename__ = "claim_status"

    claim_status_id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(30), nullable=False, unique=True)

    def __repr__(self):
        return self.description
