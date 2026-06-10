from sqlalchemy import Column, Integer, Numeric, ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import relationship
from src.database.connection import Base


class ReinsuranceParticipation(Base):
    """Modelo Python equivalente a models.ReinsuranceParticipation.java"""
    __tablename__ = "reinsurance_participation"

    participation_id = Column(Integer, primary_key=True, autoincrement=True)
    reinsurer_id = Column(Integer, ForeignKey("reinsurer.reinsurer_id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    insurance_type_id = Column(Integer, ForeignKey("insurance_type.insurance_type_id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    participation_percentage = Column(Numeric(5, 2), nullable=False)

    __table_args__ = (
        UniqueConstraint("reinsurer_id", "insurance_type_id", name="uq_participation"),
        CheckConstraint("participation_percentage > 0 AND participation_percentage <= 100", name="ck_participation_percentage"),
    )

    reinsurer = relationship("Reinsurer", back_populates="participations")
    insurance_type = relationship("InsuranceType")

    def __repr__(self):
        return f"{self.participation_percentage}%"
