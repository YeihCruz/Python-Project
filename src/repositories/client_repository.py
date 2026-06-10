from sqlalchemy.orm import Session
from src.models.client import Client
from src.repositories.base_repository import BaseRepository


class ClientRepository(BaseRepository[Client]):
    def __init__(self, session: Session):
        super().__init__(Client, session)
