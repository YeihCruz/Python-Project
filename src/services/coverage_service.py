from src.database.connection import get_db
from src.repositories.coverage_repository import CoverageRepository


class CoverageService:
    def create(self, **kwargs):
        with get_db() as db:
            repo = CoverageRepository(db)
            coverage = repo.create(**kwargs)
            db.commit()
            return coverage

    def get_by_id(self, coverage_id: int):
        with get_db() as db:
            repo = CoverageRepository(db)
            return repo.get_by_id(coverage_id)

    def get_all(self):
        with get_db() as db:
            repo = CoverageRepository(db)
            return repo.get_all()

    def update(self, coverage_id: int, **kwargs):
        with get_db() as db:
            repo = CoverageRepository(db)
            coverage = repo.update(coverage_id, **kwargs)
            if coverage:
                db.commit()
            return coverage

    def delete(self, coverage_id: int):
        with get_db() as db:
            repo = CoverageRepository(db)
            result = repo.delete(coverage_id)
            if result:
                db.commit()
            return result
