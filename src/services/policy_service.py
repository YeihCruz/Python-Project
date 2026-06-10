from src.database.connection import get_db
from src.repositories.policy_repository import PolicyRepository


class PolicyService:
    def create(self, **kwargs):
        with get_db() as db:
            repo = PolicyRepository(db)
            policy = repo.create(**kwargs)
            db.commit()
            return policy

    def get_by_id(self, policy_number: int):
        with get_db() as db:
            repo = PolicyRepository(db)
            return repo.get_by_id(policy_number)

    def get_all(self):
        with get_db() as db:
            repo = PolicyRepository(db)
            return repo.get_all()

    def update(self, policy_number: int, **kwargs):
        with get_db() as db:
            repo = PolicyRepository(db)
            policy = repo.update(policy_number, **kwargs)
            if policy:
                db.commit()
            return policy

    def delete(self, policy_number: int):
        with get_db() as db:
            repo = PolicyRepository(db)
            result = repo.delete(policy_number)
            if result:
                db.commit()
            return result
