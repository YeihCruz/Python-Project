from src.database.connection import get_db
from src.repositories.country_repository import CountryRepository


class CountryService:
    def create(self, **kwargs):
        with get_db() as db:
            repo = CountryRepository(db)
            country = repo.create(**kwargs)
            db.commit()
            return country

    def get_by_id(self, country_id: int):
        with get_db() as db:
            repo = CountryRepository(db)
            return repo.get_by_id(country_id)

    def get_all(self):
        with get_db() as db:
            repo = CountryRepository(db)
            return repo.get_all()

    def update(self, country_id: int, **kwargs):
        with get_db() as db:
            repo = CountryRepository(db)
            country = repo.update(country_id, **kwargs)
            if country:
                db.commit()
            return country

    def delete(self, country_id: int):
        with get_db() as db:
            repo = CountryRepository(db)
            result = repo.delete(country_id)
            if result:
                db.commit()
            return result
