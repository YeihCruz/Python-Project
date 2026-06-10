from sqlalchemy.orm import Session
from src.models.gender import Gender
from src.repositories.base_repository import BaseRepository


class GenderRepository(BaseRepository[Gender]):
    def __init__(self, session: Session):
        super().__init__(Gender, session)
