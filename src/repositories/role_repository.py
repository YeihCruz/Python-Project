from sqlalchemy.orm import Session
from src.models.role import Role
from src.repositories.base_repository import BaseRepository


class RoleRepository(BaseRepository[Role]):
    def __init__(self, session: Session):
        super().__init__(Role, session)
