from src.database.connection import get_db
from src.repositories.reinsurance_participation_repository import ReinsuranceParticipationRepository


class ReinsuranceParticipationService:
    def create(self, **kwargs):
        with get_db() as db:
            repo = ReinsuranceParticipationRepository(db)
            participation = repo.create(**kwargs)
            db.commit()
            return participation

    def get_by_id(self, participation_id: int):
        with get_db() as db:
            repo = ReinsuranceParticipationRepository(db)
            return repo.get_by_id(participation_id)

    def get_all(self):
        with get_db() as db:
            repo = ReinsuranceParticipationRepository(db)
            return repo.get_all()

    def update(self, participation_id: int, **kwargs):
        with get_db() as db:
            repo = ReinsuranceParticipationRepository(db)
            participation = repo.update(participation_id, **kwargs)
            if participation:
                db.commit()
            return participation

    def delete(self, participation_id: int):
        with get_db() as db:
            repo = ReinsuranceParticipationRepository(db)
            result = repo.delete(participation_id)
            if result:
                db.commit()
            return result
