from sqlalchemy import Column, Integer, String
from src.database.connection import Base


class InsuranceType(Base):
    """Modelo Python equivalente a models.InsuranceType.java"""
    __tablename__ = "insurance_type"

    insurance_type_id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(50), nullable=False, unique=True)

    def __repr__(self):
        return self.description
