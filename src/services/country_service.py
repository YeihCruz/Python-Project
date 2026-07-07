import re
from sqlalchemy.exc import IntegrityError
from src.database.connection import get_db
from src.repositories.country_repository import CountryRepository
from src.models.country import Country
from src.services.base_service import BaseService
from src.services.exceptions import ValidationError, RelatedRecordsExistError


class CountryService(BaseService):
    MAX_NAME = 80
    ISO_LENGTH = 2
    ISO_PATTERN = re.compile(r"^[A-Z]{2}$")

    def _validate_iso_code(self, iso_code: str) -> str:
        if not iso_code or not iso_code.strip():
            raise ValidationError("El código ISO es obligatorio.")
        code = iso_code.strip().upper()
        if len(code) != self.ISO_LENGTH:
            raise ValidationError(
                "El código ISO debe tener exactamente 2 caracteres."
            )
        if not self.ISO_PATTERN.match(code):
            raise ValidationError(
                "El código ISO solo puede contener letras (A-Z)."
            )
        return code

    def _validate_create(self, **kwargs) -> tuple:
        name = self.validate_required(kwargs.get("name"), "Nombre")

        # ✔ SOLO LETRAS
        name = self.validate_only_letters(name, "Nombre")

        self.validate_string_length(name, "Nombre", max_len=self.MAX_NAME)

        iso_code = self._validate_iso_code(kwargs.get("iso_code", ""))

        return name, iso_code

    def _validate_update(self, **kwargs) -> None:
        if "name" in kwargs:
            name = self.validate_required(kwargs["name"], "Nombre")
            name = self.validate_only_letters(name, "Nombre")
            self.validate_string_length(name, "Nombre", max_len=self.MAX_NAME)
            kwargs["name"] = name

    def create(self, **kwargs):
        name, iso_code = self._validate_create(**kwargs)
        with get_db() as db:
            try:
                self.check_duplicate(db, Country, "name", name)
                self.check_duplicate(db, Country, "iso_code", iso_code)
                kwargs_safe = dict(kwargs)
                kwargs_safe["name"] = name
                kwargs_safe["iso_code"] = iso_code
                repo = CountryRepository(db)
                instance = repo.create(**kwargs_safe)
                db.commit()
                return instance
            except Exception:
                db.rollback()
                raise

    def get_by_id(self, country_id: int):
        with get_db() as db:
            repo = CountryRepository(db)
            return repo.get_by_id(country_id)

    def get_all(self):
        with get_db() as db:
            repo = CountryRepository(db)
            return repo.get_all()

    def update(self, country_id: int, **kwargs):
        self._validate_update(**kwargs)
        with get_db() as db:
            try:
                self.get_or_404(db, Country, country_id, "País")
                if "name" in kwargs:
                    self.check_duplicate(
                        db, Country, "name",
                        kwargs["name"], exclude_id=country_id
                    )
                if "iso_code" in kwargs:
                    self.check_duplicate(
                        db, Country, "iso_code",
                        kwargs["iso_code"], exclude_id=country_id
                    )
                repo = CountryRepository(db)
                instance = repo.update(country_id, **kwargs)
                db.commit()
                return instance
            except Exception:
                db.rollback()
                raise

    def delete(self, country_id: int):
        with get_db() as db:
            try:
                self.get_or_404(db, Country, country_id, "País")
                repo = CountryRepository(db)
                result = repo.delete(country_id)
                db.commit()
                return result
            except IntegrityError:
                db.rollback()
                raise RelatedRecordsExistError(
                    "No se puede eliminar el país porque tiene clientes o reaseguradoras asociadas."
                )
            except Exception:
                db.rollback()
                raise
