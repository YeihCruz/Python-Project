from src.database.connection import get_db
from src.repositories.insurance_type_repository import InsuranceTypeRepository


class InsuranceTypeService:
    def create(self, **kwargs):
        with get_db() as db:
            repo = InsuranceTypeRepository(db)
            insurance_type = repo.create(**kwargs)
            db.commit()
            return insurance_type

    def get_by_id(self, insurance_type_id: int):
        with get_db() as db:
            repo = InsuranceTypeRepository(db)
            return repo.get_by_id(insurance_type_id)

    def get_all(self):
        with get_db() as db:
            repo = InsuranceTypeRepository(db)
            return repo.get_all()

    def update(self, insurance_type_id: int, **kwargs):
        with get_db() as db:
            repo = InsuranceTypeRepository(db)
            insurance_type = repo.update(insurance_type_id, **kwargs)
            if insurance_type:
                db.commit()
            return insurance_type

    def delete(self, insurance_type_id: int):
        with get_db() as db:
            repo = InsuranceTypeRepository(db)
            result = repo.delete(insurance_type_id)
            if result:
                db.commit()
            return result
