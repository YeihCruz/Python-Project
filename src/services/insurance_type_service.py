from sqlalchemy.exc import IntegrityError
from src.database.connection import get_db
from src.repositories.insurance_type_repository import InsuranceTypeRepository
from src.models.insurance_type import InsuranceType
from src.services.base_service import BaseService
from src.services.exceptions import RelatedRecordsExistError


class InsuranceTypeService(BaseService):
    MAX_DESC = 50

    def _validate_create(self, **kwargs) -> str:
        description = self.validate_description(
            kwargs.get("description"),
            "Descripción"
        )

        self.validate_string_length(
            description,
            "Descripción",
            max_len=self.MAX_DESC
        )

        return description

    def _validate_update(self, **kwargs) -> None:
        if "description" not in kwargs:
            return
        description = self.validate_description(
            kwargs.get("description"),
            "Descripción"
        )
        self.validate_string_length(description, "Descripción", max_len=self.MAX_DESC)

    def create(self, **kwargs):
        description = self._validate_create(**kwargs)
        with get_db() as db:
            try:
                self.check_duplicate(db, InsuranceType, "description", description)
                repo = InsuranceTypeRepository(db)
                instance = repo.create(description=description)
                db.commit()
                return instance
            except Exception:
                db.rollback()
                raise

    def get_by_id(self, insurance_type_id: int):
        with get_db() as db:
            repo = InsuranceTypeRepository(db)
            return repo.get_by_id(insurance_type_id)

    def get_all(self):
        with get_db() as db:
            repo = InsuranceTypeRepository(db)
            return repo.get_all()

    def update(self, insurance_type_id: int, **kwargs):
        self._validate_update(**kwargs)
        with get_db() as db:
            try:
                self.get_or_404(db, InsuranceType, insurance_type_id, "Tipo de Seguro")
                if "description" in kwargs:
                    self.check_duplicate(
                        db, InsuranceType, "description",
                        kwargs["description"], exclude_id=insurance_type_id
                    )
                repo = InsuranceTypeRepository(db)
                instance = repo.update(insurance_type_id, **kwargs)
                db.commit()
                return instance
            except Exception:
                db.rollback()
                raise

    def delete(self, insurance_type_id: int):
        with get_db() as db:
            try:
                self.get_or_404(db, InsuranceType, insurance_type_id, "Tipo de Seguro")
                repo = InsuranceTypeRepository(db)
                result = repo.delete(insurance_type_id)
                db.commit()
                return result
            except IntegrityError:
                db.rollback()
                raise RelatedRecordsExistError(
                    "No se puede eliminar el tipo porque tiene pólizas o participaciones asociadas."
                )
            except Exception:
                db.rollback()
                raise
