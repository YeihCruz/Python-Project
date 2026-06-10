from sqlalchemy.orm import Session
from src.models.reinsurance_participation import ReinsuranceParticipation
from src.repositories.base_repository import BaseRepository


class ReinsuranceParticipationRepository(BaseRepository[ReinsuranceParticipation]):
    def __init__(self, session: Session):
        super().__init__(ReinsuranceParticipation, session)
