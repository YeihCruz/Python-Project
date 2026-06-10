from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.models.user import User
from src.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: Session):
        super().__init__(User, session)

    def get_by_username(self, username: str) -> Optional[User]:
        result = self.session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    def exists_admin(self) -> bool:
        result = self.session.execute(select(User).where(User.role_id == 1).limit(1))
        return result.scalar_one_or_none() is not None
