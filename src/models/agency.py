from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database.connection import Base


class Agency(Base):
    """Modelo Python equivalente a models.Agency.java"""
    __tablename__ = "agency"

    agency_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    address = Column(String(200), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    general_director = Column(String(100), nullable=False)
    insurance_manager = Column(String(100), nullable=False)
    claims_manager = Column(String(100), nullable=False)

    clients = relationship("Client", back_populates="agency")
    reinsurers = relationship("Reinsurer", back_populates="agency")

    def __repr__(self):
        return self.name
