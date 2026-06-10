from sqlalchemy.orm import Session
from src.models.claim import Claim
from src.repositories.base_repository import BaseRepository


class ClaimRepository(BaseRepository[Claim]):
    def __init__(self, session: Session):
        super().__init__(Claim, session)
