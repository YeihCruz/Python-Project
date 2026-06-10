from src.database.connection import get_db
from src.repositories.client_repository import ClientRepository


class ClientService:
    def create(self, **kwargs):
        with get_db() as db:
            repo = ClientRepository(db)
            client = repo.create(**kwargs)
            db.commit()
            return client

    def get_by_id(self, client_id: int):
        with get_db() as db:
            repo = ClientRepository(db)
            return repo.get_by_id(client_id)

    def get_all(self):
        with get_db() as db:
            repo = ClientRepository(db)
            return repo.get_all()

    def update(self, client_id: int, **kwargs):
        with get_db() as db:
            repo = ClientRepository(db)
            client = repo.update(client_id, **kwargs)
            if client:
                db.commit()
            return client

    def delete(self, client_id: int):
        with get_db() as db:
            repo = ClientRepository(db)
            result = repo.delete(client_id)
            if result:
                db.commit()
            return result
