from sqlalchemy.exc import IntegrityError
from src.database.connection import get_db
from src.repositories.claim_status_repository import ClaimStatusRepository
from src.models.claim_status import ClaimStatus
from src.services.base_service import BaseService
from src.services.exceptions import NotFoundError, RelatedRecordsExistError


class ClaimStatusService(BaseService):
    MAX_DESC = 30

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

    def _validate_update(self, claim_status_id: int, **kwargs) -> dict:
        data = {}

        if "description" in kwargs:
            description = self.validate_description(
                kwargs["description"],
                "Descripción"
            )

            self.validate_string_length(
                description,
                "Descripción",
                max_len=self.MAX_DESC
            )

            data["description"] = description

        return data

    def create(self, **kwargs):
        description = self._validate_create(**kwargs)
        with get_db() as db:
            try:
                self.check_duplicate(db, ClaimStatus, "description", description)
                repo = ClaimStatusRepository(db)
                instance = repo.create(description=description)
                db.commit()
                return instance
            except Exception:
                db.rollback()
                raise

    def get_by_id(self, claim_status_id: int):
        with get_db() as db:
            repo = ClaimStatusRepository(db)
            return repo.get_by_id(claim_status_id)

    def get_all(self):
        with get_db() as db:
            repo = ClaimStatusRepository(db)
            return repo.get_all()

    def update(self, claim_status_id: int, **kwargs):
        validated = self._validate_update(
            claim_status_id,
            **kwargs
        )

        with get_db() as db:
            try:
                self.get_or_404(
                    db,
                    ClaimStatus,
                    claim_status_id,
                    "Estado de Reclamo"
                )

                if "description" in validated:
                    self.check_duplicate(
                        db,
                        ClaimStatus,
                        "description",
                        validated["description"],
                        exclude_id=claim_status_id
                    )

                repo = ClaimStatusRepository(db)

                instance = repo.update(
                    claim_status_id,
                    **validated
                )

                db.commit()
                return instance

            except Exception:
                db.rollback()
                raise

    def delete(self, claim_status_id: int):
        with get_db() as db:
            try:
                self.get_or_404(db, ClaimStatus, claim_status_id, "Estado de Reclamo")
                repo = ClaimStatusRepository(db)
                result = repo.delete(claim_status_id)
                db.commit()
                return result
            except IntegrityError:
                db.rollback()
                raise RelatedRecordsExistError(
                    "No se puede eliminar el estado porque tiene reclamos asociados."
                )
            except Exception:
                db.rollback()
                raise
