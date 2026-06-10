from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey
from sqlalchemy.orm import relationship
from src.database.connection import Base


class Client(Base):
    """Modelo Python equivalente a models.Client.java"""
    __tablename__ = "client"

    client_id = Column(Integer, primary_key=True, autoincrement=True)
    agency_id = Column(Integer, ForeignKey("agency.agency_id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    gender_id = Column(Integer, ForeignKey("gender.gender_id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    country_id = Column(Integer, ForeignKey("country.country_id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    first_name = Column(String(80), nullable=False)
    last_name = Column(String(100), nullable=False)
    identification_number = Column(String(30), nullable=False, unique=True)
    age = Column(SmallInteger, nullable=False)
    address = Column(String(200), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False, unique=True)

    agency = relationship("Agency", back_populates="clients")
    gender = relationship("Gender")
    country = relationship("Country")
    policies = relationship("Policy", back_populates="client")

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"
