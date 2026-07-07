from sqlalchemy.exc import IntegrityError
from src.database.connection import get_db
from src.repositories.coverage_repository import CoverageRepository
from src.models.coverage import Coverage
from src.models.policy import Policy
from src.services.base_service import BaseService
from src.services.exceptions import ValidationError, RelatedRecordsExistError


class CoverageService(BaseService):
    MAX_DESC = 200

    def _validate_create(self, db, **kwargs) -> dict:
        policy_number = kwargs.get("policy_number")
        if policy_number is None:
            raise ValidationError("La póliza es obligatoria.")
        self.get_or_404(db, Policy, policy_number, "Póliza")

        description = self.validate_required(kwargs.get("description"), "Descripción")
        self.validate_string_length(description, "Descripción", max_len=self.MAX_DESC)

        coverage_amount = kwargs.get("coverage_amount")
        self.validate_positive_number(coverage_amount, "Monto de Cobertura")

        return dict(
            policy_number=policy_number, description=description,
            coverage_amount=coverage_amount,
        )

    def _validate_update(self, db, **kwargs) -> None:
        if "policy_number" in kwargs:
            self.get_or_404(db, Policy, kwargs["policy_number"], "Póliza")
        if "description" in kwargs:
            val = self.validate_required(kwargs["description"], "Descripción")
            self.validate_string_length(val, "Descripción", max_len=self.MAX_DESC)
        if "coverage_amount" in kwargs:
            self.validate_positive_number(kwargs["coverage_amount"], "Monto de Cobertura")

    def create(self, **kwargs):
        with get_db() as db:
            try:
                validated = self._validate_create(db, **kwargs)
                kwargs_full = dict(kwargs)
                kwargs_full.update(validated)
                repo = CoverageRepository(db)
                instance = repo.create(**kwargs_full)
                db.commit()
                return instance
            except Exception:
                db.rollback()
                raise

    def get_by_id(self, coverage_id: int):
        with get_db() as db:
            repo = CoverageRepository(db)
            return repo.get_by_id(coverage_id)

    def get_all(self):
        with get_db() as db:
            repo = CoverageRepository(db)
            return repo.get_all()

    def update(self, coverage_id: int, **kwargs):
        with get_db() as db:
            try:
                self.get_or_404(db, Coverage, coverage_id, "Cobertura")
                self._validate_update(db, **kwargs)
                repo = CoverageRepository(db)
                instance = repo.update(coverage_id, **kwargs)
                db.commit()
                return instance
            except Exception:
                db.rollback()
                raise

    def delete(self, coverage_id: int):
        with get_db() as db:
            try:
                self.get_or_404(db, Coverage, coverage_id, "Cobertura")
                repo = CoverageRepository(db)
                result = repo.delete(coverage_id)
                db.commit()
                return result
            except IntegrityError:
                db.rollback()
                raise RelatedRecordsExistError(
                    "No se puede eliminar la cobertura porque tiene registros asociados."
                )
            except Exception:
                db.rollback()
                raise
