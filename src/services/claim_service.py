from src.database.connection import get_db
from src.repositories.claim_repository import ClaimRepository


class ClaimService:
    def create(self, **kwargs):
        with get_db() as db:
            repo = ClaimRepository(db)
            claim = repo.create(**kwargs)
            db.commit()
            return claim

    def get_by_id(self, claim_number: int):
        with get_db() as db:
            repo = ClaimRepository(db)
            return repo.get_by_id(claim_number)

    def get_all(self):
        with get_db() as db:
            repo = ClaimRepository(db)
            return repo.get_all()

    def update(self, claim_number: int, **kwargs):
        with get_db() as db:
            repo = ClaimRepository(db)
            claim = repo.update(claim_number, **kwargs)
            if claim:
                db.commit()
            return claim

    def delete(self, claim_number: int):
        with get_db() as db:
            repo = ClaimRepository(db)
            result = repo.delete(claim_number)
            if result:
                db.commit()
            return result
