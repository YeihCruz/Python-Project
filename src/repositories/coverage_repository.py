from sqlalchemy.orm import Session
from src.models.coverage import Coverage
from src.repositories.base_repository import BaseRepository


class CoverageRepository(BaseRepository[Coverage]):
    def __init__(self, session: Session):
        super().__init__(Coverage, session)
