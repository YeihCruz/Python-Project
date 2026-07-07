from sqlalchemy.exc import IntegrityError
from src.database.connection import get_db
from src.repositories.gender_repository import GenderRepository
from src.models.gender import Gender
from src.services.base_service import BaseService
from src.services.exceptions import RelatedRecordsExistError


class GenderService(BaseService):
    MAX_DESC = 20

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
                self.check_duplicate(db, Gender, "description", description)
                repo = GenderRepository(db)
                instance = repo.create(description=description)
                db.commit()
                return instance
            except Exception:
                db.rollback()
                raise

    def get_by_id(self, gender_id: int):
        with get_db() as db:
            repo = GenderRepository(db)
            return repo.get_by_id(gender_id)

    def get_all(self):
        with get_db() as db:
            repo = GenderRepository(db)
            return repo.get_all()

    def update(self, gender_id: int, **kwargs):
        self._validate_update(**kwargs)
        with get_db() as db:
            try:
                self.get_or_404(db, Gender, gender_id, "Género")
                if "description" in kwargs:
                    self.check_duplicate(
                        db, Gender, "description",
                        kwargs["description"], exclude_id=gender_id
                    )
                repo = GenderRepository(db)
                instance = repo.update(gender_id, **kwargs)
                db.commit()
                return instance
            except Exception:
                db.rollback()
                raise

    def delete(self, gender_id: int):
        with get_db() as db:
            try:
                self.get_or_404(db, Gender, gender_id, "Género")
                repo = GenderRepository(db)
                result = repo.delete(gender_id)
                db.commit()
                return result
            except IntegrityError:
                db.rollback()
                raise RelatedRecordsExistError(
                    "No se puede eliminar el género porque tiene clientes asociados."
                )
            except Exception:
                db.rollback()
                raise
