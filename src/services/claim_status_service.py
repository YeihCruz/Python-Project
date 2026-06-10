from src.database.connection import get_db
from src.repositories.claim_status_repository import ClaimStatusRepository


class ClaimStatusService:
    def create(self, **kwargs):
        with get_db() as db:
            repo = ClaimStatusRepository(db)
            claim_status = repo.create(**kwargs)
            db.commit()
            return claim_status

    def get_by_id(self, claim_status_id: int):
        with get_db() as db:
            repo = ClaimStatusRepository(db)
            return repo.get_by_id(claim_status_id)

    def get_all(self):
        with get_db() as db:
            repo = ClaimStatusRepository(db)
            return repo.get_all()

    def update(self, claim_status_id: int, **kwargs):
        with get_db() as db:
            repo = ClaimStatusRepository(db)
            claim_status = repo.update(claim_status_id, **kwargs)
            if claim_status:
                db.commit()
            return claim_status

    def delete(self, claim_status_id: int):
        with get_db() as db:
            repo = ClaimStatusRepository(db)
            result = repo.delete(claim_status_id)
            if result:
                db.commit()
            return result
