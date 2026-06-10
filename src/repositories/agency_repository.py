from sqlalchemy.orm import Session
from src.models.agency import Agency
from src.repositories.base_repository import BaseRepository


class AgencyRepository(BaseRepository[Agency]):
    def __init__(self, session: Session):
        super().__init__(Agency, session)
