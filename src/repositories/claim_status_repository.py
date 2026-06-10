from sqlalchemy.orm import Session
from src.models.claim_status import ClaimStatus
from src.repositories.base_repository import BaseRepository


class ClaimStatusRepository(BaseRepository[ClaimStatus]):
    def __init__(self, session: Session):
        super().__init__(ClaimStatus, session)
