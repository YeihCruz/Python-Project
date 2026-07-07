from sqlalchemy.exc import IntegrityError
from src.database.connection import get_db
from src.repositories.reinsurance_type_repository import ReinsuranceTypeRepository
from src.models.reinsurance_type import ReinsuranceType
from src.services.base_service import BaseService
from src.services.exceptions import RelatedRecordsExistError


class ReinsuranceTypeService(BaseService):
    MAX_DESC = 50

    def _validate_create(self, **kwargs) -> str:
        description = self.validate_required(kwargs.get("description"), "Descripción")

        # ✔ VALIDACIÓN CORRECTA (SOLO LETRAS)
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
                self.check_duplicate(db, ReinsuranceType, "description", description)
                repo = ReinsuranceTypeRepository(db)
                instance = repo.create(description=description)
                db.commit()
                return instance
            except Exception:
                db.rollback()
                raise

    def get_by_id(self, reinsurance_type_id: int):
        with get_db() as db:
            repo = ReinsuranceTypeRepository(db)
            return repo.get_by_id(reinsurance_type_id)

    def get_all(self):
        with get_db() as db:
            repo = ReinsuranceTypeRepository(db)
            return repo.get_all()

    def update(self, reinsurance_type_id: int, **kwargs):
        self._validate_update(**kwargs)
        with get_db() as db:
            try:
                self.get_or_404(db, ReinsuranceType, reinsurance_type_id, "Tipo de Reaseguro")
                if "description" in kwargs:
                    self.check_duplicate(
                        db, ReinsuranceType, "description",
                        kwargs["description"], exclude_id=reinsurance_type_id
                    )
                repo = ReinsuranceTypeRepository(db)
                instance = repo.update(reinsurance_type_id, **kwargs)
                db.commit()
                return instance
            except Exception:
                db.rollback()
                raise

    def delete(self, reinsurance_type_id: int):
        with get_db() as db:
            try:
                self.get_or_404(db, ReinsuranceType, reinsurance_type_id, "Tipo de Reaseguro")
                repo = ReinsuranceTypeRepository(db)
                result = repo.delete(reinsurance_type_id)
                db.commit()
                return result
            except IntegrityError:
                db.rollback()
                raise RelatedRecordsExistError(
                    "No se puede eliminar el tipo porque tiene reaseguradoras asociadas."
                )
            except Exception:
                db.rollback()
                raise
