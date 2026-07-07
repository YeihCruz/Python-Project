from sqlalchemy.exc import IntegrityError
from src.database.connection import get_db
from src.repositories.policy_status_repository import PolicyStatusRepository
from src.models.policy_status import PolicyStatus
from src.services.base_service import BaseService
from src.services.exceptions import RelatedRecordsExistError


class PolicyStatusService(BaseService):
    MAX_DESC = 30

    def _validate_create(self, **kwargs) -> str:
        description = self.validate_required(kwargs.get("description"), "Descripción")

        # ✔️ ESTA ES LA VALIDACIÓN CORRECTA (SOLO LETRAS)
        description = self.validate_only_letters(description, "Descripción")

        self.validate_string_length(
            description,
            "Descripción",
            max_len=self.MAX_DESC
        )

        return description

    def _validate_update(self, **kwargs) -> None:
        if "description" not in kwargs:
            return

        description = self.validate_required(kwargs.get("description"), "Descripción")

        # ✔️ MISMA VALIDACIÓN AQUÍ
        description = self.validate_only_letters(description, "Descripción")

        self.validate_string_length(
            description,
            "Descripción",
            max_len=self.MAX_DESC
        )

    def create(self, **kwargs):
        description = self._validate_create(**kwargs)
        with get_db() as db:
            try:
                self.check_duplicate(db, PolicyStatus, "description", description)
                repo = PolicyStatusRepository(db)
                instance = repo.create(description=description)
                db.commit()
                return instance
            except Exception:
                db.rollback()
                raise

    def get_by_id(self, policy_status_id: int):
        with get_db() as db:
            repo = PolicyStatusRepository(db)
            return repo.get_by_id(policy_status_id)

    def get_all(self):
        with get_db() as db:
            repo = PolicyStatusRepository(db)
            return repo.get_all()

    def update(self, policy_status_id: int, **kwargs):
        self._validate_update(**kwargs)
        with get_db() as db:
            try:
                self.get_or_404(db, PolicyStatus, policy_status_id, "Estado de Póliza")
                if "description" in kwargs:
                    self.check_duplicate(
                        db, PolicyStatus, "description",
                        kwargs["description"], exclude_id=policy_status_id
                    )
                repo = PolicyStatusRepository(db)
                instance = repo.update(policy_status_id, **kwargs)
                db.commit()
                return instance
            except Exception:
                db.rollback()
                raise

    def delete(self, policy_status_id: int):
        with get_db() as db:
            try:
                self.get_or_404(db, PolicyStatus, policy_status_id, "Estado de Póliza")
                repo = PolicyStatusRepository(db)
                result = repo.delete(policy_status_id)
                db.commit()
                return result
            except IntegrityError:
                db.rollback()
                raise RelatedRecordsExistError(
                    "No se puede eliminar el estado porque tiene pólizas asociadas."
                )
            except Exception:
                db.rollback()
                raise
