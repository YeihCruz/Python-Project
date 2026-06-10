from src.database.connection import get_db
from src.repositories.claim_type_repository import ClaimTypeRepository


class ClaimTypeService:
    def create(self, **kwargs):
        with get_db() as db:
            repo = ClaimTypeRepository(db)
            claim_type = repo.create(**kwargs)
            db.commit()
            return claim_type

    def get_by_id(self, claim_type_id: int):
        with get_db() as db:
            repo = ClaimTypeRepository(db)
            return repo.get_by_id(claim_type_id)

    def get_all(self):
        with get_db() as db:
            repo = ClaimTypeRepository(db)
            return repo.get_all()

    def update(self, claim_type_id: int, **kwargs):
        with get_db() as db:
            repo = ClaimTypeRepository(db)
            claim_type = repo.update(claim_type_id, **kwargs)
            if claim_type:
                db.commit()
            return claim_type

    def delete(self, claim_type_id: int):
        with get_db() as db:
            repo = ClaimTypeRepository(db)
            result = repo.delete(claim_type_id)
            if result:
                db.commit()
            return result
