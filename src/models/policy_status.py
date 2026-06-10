from sqlalchemy import Column, Integer, String
from src.database.connection import Base


class PolicyStatus(Base):
    """Modelo Python equivalente a models.PolicyStatus.java"""
    __tablename__ = "policy_status"

    policy_status_id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(30), nullable=False, unique=True)

    def __repr__(self):
        return self.description
