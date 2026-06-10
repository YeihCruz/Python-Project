from sqlalchemy.orm import Session
from src.models.reinsurer import Reinsurer
from src.repositories.base_repository import BaseRepository


class ReinsurerRepository(BaseRepository[Reinsurer]):
    def __init__(self, session: Session):
        super().__init__(Reinsurer, session)
