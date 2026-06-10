from sqlalchemy.orm import Session
from src.models.reinsurance_type import ReinsuranceType
from src.repositories.base_repository import BaseRepository


class ReinsuranceTypeRepository(BaseRepository[ReinsuranceType]):
    def __init__(self, session: Session):
        super().__init__(ReinsuranceType, session)
