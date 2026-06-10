from src.database.connection import get_db
from src.repositories.role_repository import RoleRepository


class RoleService:
    def create(self, **kwargs):
        with get_db() as db:
            repo = RoleRepository(db)
            role = repo.create(**kwargs)
            db.commit()
            return role

    def get_by_id(self, role_id: int):
        with get_db() as db:
            repo = RoleRepository(db)
            return repo.get_by_id(role_id)

    def get_all(self):
        with get_db() as db:
            repo = RoleRepository(db)
            return repo.get_all()

    def update(self, role_id: int, **kwargs):
        with get_db() as db:
            repo = RoleRepository(db)
            role = repo.update(role_id, **kwargs)
            if role:
                db.commit()
            return role

    def delete(self, role_id: int):
        with get_db() as db:
            repo = RoleRepository(db)
            result = repo.delete(role_id)
            if result:
                db.commit()
            return result
