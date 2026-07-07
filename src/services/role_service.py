from sqlalchemy.exc import IntegrityError
from src.database.connection import get_db
from src.repositories.role_repository import RoleRepository
from src.models.role import Role
from src.services.base_service import BaseService
from src.services.exceptions import RelatedRecordsExistError


class RoleService(BaseService):
    MAX_NAME = 50

    def _validate_create(self, **kwargs) -> str:
        name = self.validate_required(kwargs.get("name"), "Nombre")
        self.validate_string_length(name, "Nombre", max_len=self.MAX_NAME)
        return name

    def _validate_update(self, **kwargs) -> None:
        if "name" not in kwargs:
            return
        name = self.validate_required(kwargs["name"], "Nombre")
        self.validate_string_length(name, "Nombre", max_len=self.MAX_NAME)

    def create(self, **kwargs):
        name = self._validate_create(**kwargs)
        with get_db() as db:
            try:
                self.check_duplicate(db, Role, "name", name)
                repo = RoleRepository(db)
                instance = repo.create(name=name)
                db.commit()
                return instance
            except Exception:
                db.rollback()
                raise

    def get_by_id(self, role_id: int):
        with get_db() as db:
            repo = RoleRepository(db)
            return repo.get_by_id(role_id)

    def get_all(self):
        with get_db() as db:
            repo = RoleRepository(db)
            return repo.get_all()

    def update(self, role_id: int, **kwargs):
        self._validate_update(**kwargs)
        with get_db() as db:
            try:
                self.get_or_404(db, Role, role_id, "Rol")
                if "name" in kwargs:
                    self.check_duplicate(
                        db, Role, "name",
                        kwargs["name"], exclude_id=role_id
                    )
                repo = RoleRepository(db)
                instance = repo.update(role_id, **kwargs)
                db.commit()
                return instance
            except Exception:
                db.rollback()
                raise

    def delete(self, role_id: int):
        with get_db() as db:
            try:
                self.get_or_404(db, Role, role_id, "Rol")
                repo = RoleRepository(db)
                result = repo.delete(role_id)
                db.commit()
                return result
            except IntegrityError:
                db.rollback()
                raise RelatedRecordsExistError(
                    "No se puede eliminar el rol porque tiene usuarios asociados."
                )
            except Exception:
                db.rollback()
                raise
