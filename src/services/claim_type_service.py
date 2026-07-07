from sqlalchemy.exc import IntegrityError
from src.database.connection import get_db
from src.repositories.claim_type_repository import ClaimTypeRepository
from src.models.claim_type import ClaimType
from src.services.base_service import BaseService
from src.services.exceptions import RelatedRecordsExistError


class ClaimTypeService(BaseService):
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

        self.validate_string_length(
            description,
            "Descripción",
            max_len=self.MAX_DESC
        )

        kwargs["description"] = description
    def create(self, **kwargs):
        description = self._validate_create(**kwargs)
        with get_db() as db:
            try:
                self.check_duplicate(db, ClaimType, "description", description)
                repo = ClaimTypeRepository(db)
                instance = repo.create(description=description)
                db.commit()
                return instance
            except Exception:
                db.rollback()
                raise

    def get_by_id(self, claim_type_id: int):
        with get_db() as db:
            repo = ClaimTypeRepository(db)
            return repo.get_by_id(claim_type_id)

    def get_all(self):
        with get_db() as db:
            repo = ClaimTypeRepository(db)
            return repo.get_all()

    def update(self, claim_type_id: int, **kwargs):
        self._validate_update(**kwargs)
        with get_db() as db:
            try:
                self.get_or_404(db, ClaimType, claim_type_id, "Tipo de Reclamo")
                if "description" in kwargs:
                    self.check_duplicate(
                        db, ClaimType, "description",
                        kwargs["description"], exclude_id=claim_type_id
                    )
                repo = ClaimTypeRepository(db)
                instance = repo.update(claim_type_id, **kwargs)
                db.commit()
                return instance
            except Exception:
                db.rollback()
                raise

    def delete(self, claim_type_id: int):
        with get_db() as db:
            try:
                self.get_or_404(db, ClaimType, claim_type_id, "Tipo de Reclamo")
                repo = ClaimTypeRepository(db)
                result = repo.delete(claim_type_id)
                db.commit()
                return result
            except IntegrityError:
                db.rollback()
                raise RelatedRecordsExistError(
                    "No se puede eliminar el tipo porque tiene reclamos asociados."
                )
            except Exception:
                db.rollback()
                raise
