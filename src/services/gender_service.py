from src.database.connection import get_db
from src.repositories.gender_repository import GenderRepository


class GenderService:
    def create(self, **kwargs):
        with get_db() as db:
            repo = GenderRepository(db)
            gender = repo.create(**kwargs)
            db.commit()
            return gender

    def get_by_id(self, gender_id: int):
        with get_db() as db:
            repo = GenderRepository(db)
            return repo.get_by_id(gender_id)

    def get_all(self):
        with get_db() as db:
            repo = GenderRepository(db)
            return repo.get_all()

    def update(self, gender_id: int, **kwargs):
        with get_db() as db:
            repo = GenderRepository(db)
            gender = repo.update(gender_id, **kwargs)
            if gender:
                db.commit()
            return gender

    def delete(self, gender_id: int):
        with get_db() as db:
            repo = GenderRepository(db)
            result = repo.delete(gender_id)
            if result:
                db.commit()
            return result
