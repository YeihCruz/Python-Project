from sqlalchemy import Column, Integer, Date, Numeric, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from src.database.connection import Base


class Policy(Base):
    """Modelo Python equivalente a models.Policy.java"""
    __tablename__ = "policy"

    policy_number = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("client.client_id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    insurance_type_id = Column(Integer, ForeignKey("insurance_type.insurance_type_id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    policy_status_id = Column(Integer, ForeignKey("policy_status.policy_status_id", onupdate="CASCADE", ondelete="RESTRICT"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    monthly_premium = Column(Numeric(12, 2), nullable=False)
    insured_amount = Column(Numeric(14, 2), nullable=False)
    cancellation_reason = Column(String(300), nullable=True)

    __table_args__ = (
        CheckConstraint("end_date > start_date", name="ck_policy_dates"),
        CheckConstraint("monthly_premium > 0", name="ck_policy_premium"),
        CheckConstraint("insured_amount > 0", name="ck_policy_insured"),
    )

    client = relationship("Client", back_populates="policies")
    insurance_type = relationship("InsuranceType")
    policy_status = relationship("PolicyStatus")
    coverages = relationship("Coverage", back_populates="policy", cascade="all, delete-orphan")
    claims = relationship("Claim", back_populates="policy")

    def __repr__(self):
        return f"Policy #{self.policy_number}"
