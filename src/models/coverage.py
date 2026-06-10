from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from src.database.connection import Base


class Coverage(Base):
    """Modelo Python equivalente a models.Coverage.java"""
    __tablename__ = "coverage"

    coverage_id = Column(Integer, primary_key=True, autoincrement=True)
    policy_number = Column(Integer, ForeignKey("policy.policy_number", onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    description = Column(String(200), nullable=False)
    coverage_amount = Column(Numeric(14, 2), nullable=False)

    __table_args__ = (
        CheckConstraint("coverage_amount > 0", name="ck_coverage_amount"),
    )

    policy = relationship("Policy", back_populates="coverages")

    def __repr__(self):
        return self.description
