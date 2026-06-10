from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database.connection import Base


class Reinsurer(Base):
    """Modelo Python equivalente a models.Reinsurer.java"""
    __tablename__ = "reinsurer"

    reinsurer_id = Column(Integer, primary_key=True, autoincrement=True)
    agency_id = Column(Integer, ForeignKey("agency.agency_id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    reinsurance_type_id = Column(Integer, ForeignKey("reinsurance_type.reinsurance_type_id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    country_id = Column(Integer, ForeignKey("country.country_id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    name = Column(String(100), nullable=False, unique=True)

    agency = relationship("Agency", back_populates="reinsurers")
    reinsurance_type = relationship("ReinsuranceType")
    country = relationship("Country")
    participations = relationship("ReinsuranceParticipation", back_populates="reinsurer")

    def __repr__(self):
        return self.name
