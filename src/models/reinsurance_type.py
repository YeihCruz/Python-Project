from sqlalchemy import Column, Integer, String
from src.database.connection import Base


class ReinsuranceType(Base):
    """Modelo Python equivalente a models.ReinsuranceType.java"""
    __tablename__ = "reinsurance_type"

    reinsurance_type_id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(50), nullable=False, unique=True)

    def __repr__(self):
        return self.description
