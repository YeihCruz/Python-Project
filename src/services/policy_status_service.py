from src.database.connection import get_db
from src.repositories.policy_status_repository import PolicyStatusRepository


class PolicyStatusService:
    def create(self, **kwargs):
        with get_db() as db:
            repo = PolicyStatusRepository(db)
            policy_status = repo.create(**kwargs)
            db.commit()
            return policy_status

    def get_by_id(self, policy_status_id: int):
        with get_db() as db:
            repo = PolicyStatusRepository(db)
            return repo.get_by_id(policy_status_id)

    def get_all(self):
        with get_db() as db:
            repo = PolicyStatusRepository(db)
            return repo.get_all()

    def update(self, policy_status_id: int, **kwargs):
        with get_db() as db:
            repo = PolicyStatusRepository(db)
            policy_status = repo.update(policy_status_id, **kwargs)
            if policy_status:
                db.commit()
            return policy_status

    def delete(self, policy_status_id: int):
        with get_db() as db:
            repo = PolicyStatusRepository(db)
            result = repo.delete(policy_status_id)
            if result:
                db.commit()
            return result
