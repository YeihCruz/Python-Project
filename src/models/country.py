from sqlalchemy import Column, Integer, String
from src.database.connection import Base


class Country(Base):
    """Modelo Python equivalente a models.Country.java"""
    __tablename__ = "country"

    country_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), nullable=False, unique=True)
    iso_code = Column(String(2), nullable=False, unique=True)

    def __repr__(self):
        return self.name
