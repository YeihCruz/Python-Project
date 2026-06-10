from src.database.connection import get_db
from src.repositories.reinsurance_type_repository import ReinsuranceTypeRepository


class ReinsuranceTypeService:
    def create(self, **kwargs):
        with get_db() as db:
            repo = ReinsuranceTypeRepository(db)
            reinsurance_type = repo.create(**kwargs)
            db.commit()
            return reinsurance_type

    def get_by_id(self, reinsurance_type_id: int):
        with get_db() as db:
            repo = ReinsuranceTypeRepository(db)
            return repo.get_by_id(reinsurance_type_id)

    def get_all(self):
        with get_db() as db:
            repo = ReinsuranceTypeRepository(db)
            return repo.get_all()

    def update(self, reinsurance_type_id: int, **kwargs):
        with get_db() as db:
            repo = ReinsuranceTypeRepository(db)
            reinsurance_type = repo.update(reinsurance_type_id, **kwargs)
            if reinsurance_type:
                db.commit()
            return reinsurance_type

    def delete(self, reinsurance_type_id: int):
        with get_db() as db:
            repo = ReinsuranceTypeRepository(db)
            result = repo.delete(reinsurance_type_id)
            if result:
                db.commit()
            return result
