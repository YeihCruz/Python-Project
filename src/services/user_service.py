import hashlib
from typing import Optional
from src.database.connection import get_db
from src.repositories.user_repository import UserRepository
from src.models.user import User


class UserService:
    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def create(self, **kwargs):
        if "password" in kwargs:
            kwargs["password"] = self._hash_password(kwargs["password"])
        with get_db() as db:
            repo = UserRepository(db)
            user = repo.create(**kwargs)
            db.commit()
            return user

    def get_by_id(self, user_id: int):
        with get_db() as db:
            repo = UserRepository(db)
            return repo.get_by_id(user_id)

    def get_all(self):
        with get_db() as db:
            repo = UserRepository(db)
            return repo.get_all()

    def update(self, user_id: int, **kwargs):
        if "password" in kwargs:
            kwargs["password"] = self._hash_password(kwargs["password"])
        with get_db() as db:
            repo = UserRepository(db)
            user = repo.update(user_id, **kwargs)
            if user:
                db.commit()
            return user

    def delete(self, user_id: int):
        with get_db() as db:
            repo = UserRepository(db)
            result = repo.delete(user_id)
            if result:
                db.commit()
            return result

    def login(self, username: str, password: str) -> Optional[User]:
        hashed = self._hash_password(password)
        with get_db() as db:
            repo = UserRepository(db)
            user = repo.get_by_username(username)
            if user and user.password == hashed and user.active:
                return user
            return None

    def exists_admin(self) -> bool:
        with get_db() as db:
            repo = UserRepository(db)
            return repo.exists_admin()

    def deactivate(self, user_id: int):
        return self.update(user_id, active=False)
