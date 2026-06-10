from sqlalchemy import Column, Integer, Date, Numeric, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from src.database.connection import Base


class Claim(Base):
    """Modelo Python equivalente a models.Claim.java"""
    __tablename__ = "claim"

    claim_number = Column(Integer, primary_key=True, autoincrement=True)
    policy_number = Column(Integer, ForeignKey("policy.policy_number", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    claim_type_id = Column(Integer, ForeignKey("claim_type.claim_type_id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    claim_status_id = Column(Integer, ForeignKey("claim_status.claim_status_id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    incident_date = Column(Date, nullable=False)
    claimed_amount = Column(Numeric(14, 2), nullable=False)
    compensated_amount = Column(Numeric(14, 2), nullable=True)
    rejection_reason = Column(String(300), nullable=True)

    __table_args__ = (
        CheckConstraint("claimed_amount > 0", name="ck_claimed_amount"),
        CheckConstraint("compensated_amount >= 0", name="ck_compensated_amount"),
    )

    policy = relationship("Policy", back_populates="claims")
    claim_type = relationship("ClaimType")
    claim_status = relationship("ClaimStatus")

    def __repr__(self):
        return f"Claim #{self.claim_number}"
