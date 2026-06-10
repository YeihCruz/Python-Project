from src.database.connection import get_db
from src.repositories.reinsurer_repository import ReinsurerRepository


class ReinsurerService:
    def create(self, **kwargs):
        with get_db() as db:
            repo = ReinsurerRepository(db)
            reinsurer = repo.create(**kwargs)
            db.commit()
            return reinsurer

    def get_by_id(self, reinsurer_id: int):
        with get_db() as db:
            repo = ReinsurerRepository(db)
            return repo.get_by_id(reinsurer_id)

    def get_all(self):
        with get_db() as db:
            repo = ReinsurerRepository(db)
            return repo.get_all()

    def update(self, reinsurer_id: int, **kwargs):
        with get_db() as db:
            repo = ReinsurerRepository(db)
            reinsurer = repo.update(reinsurer_id, **kwargs)
            if reinsurer:
                db.commit()
            return reinsurer

    def delete(self, reinsurer_id: int):
        with get_db() as db:
            repo = ReinsurerRepository(db)
            result = repo.delete(reinsurer_id)
            if result:
                db.commit()
            return result
