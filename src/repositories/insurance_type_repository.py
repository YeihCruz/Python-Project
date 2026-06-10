from sqlalchemy.orm import Session
from src.models.insurance_type import InsuranceType
from src.repositories.base_repository import BaseRepository


class InsuranceTypeRepository(BaseRepository[InsuranceType]):
    def __init__(self, session: Session):
        super().__init__(InsuranceType, session)
