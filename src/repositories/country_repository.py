from sqlalchemy.orm import Session
from src.models.country import Country
from src.repositories.base_repository import BaseRepository


class CountryRepository(BaseRepository[Country]):
    def __init__(self, session: Session):
        super().__init__(Country, session)
