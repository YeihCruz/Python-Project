from sqlalchemy.orm import Session
from src.models.policy_status import PolicyStatus
from src.repositories.base_repository import BaseRepository


class PolicyStatusRepository(BaseRepository[PolicyStatus]):
    def __init__(self, session: Session):
        super().__init__(PolicyStatus, session)
