from sqlalchemy.orm import Session
from src.models.policy import Policy
from src.repositories.base_repository import BaseRepository


class PolicyRepository(BaseRepository[Policy]):
    def __init__(self, session: Session):
        super().__init__(Policy, session)
