from src.database.connection import get_db
from src.repositories.agency_repository import AgencyRepository


class AgencyService:
    def create(self, **kwargs):
        with get_db() as db:
            repo = AgencyRepository(db)
            agency = repo.create(**kwargs)
            db.commit()
            return agency

    def get_by_id(self, agency_id: int):
        with get_db() as db:
            repo = AgencyRepository(db)
            return repo.get_by_id(agency_id)

    def get_all(self):
        with get_db() as db:
            repo = AgencyRepository(db)
            return repo.get_all()

    def update(self, agency_id: int, **kwargs):
        with get_db() as db:
            repo = AgencyRepository(db)
            agency = repo.update(agency_id, **kwargs)
            if agency:
                db.commit()
            return agency

    def delete(self, agency_id: int):
        with get_db() as db:
            repo = AgencyRepository(db)
            result = repo.delete(agency_id)
            if result:
                db.commit()
            return result
