from sqlalchemy.orm import Session
from src.models.claim_type import ClaimType
from src.repositories.base_repository import BaseRepository


class ClaimTypeRepository(BaseRepository[ClaimType]):
    def __init__(self, session: Session):
        super().__init__(ClaimType, session)
