from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from src.database.connection import get_db
from src.repositories.reinsurer_repository import ReinsurerRepository
from src.models.reinsurer import Reinsurer
from src.models.agency import Agency
from src.models.reinsurance_type import ReinsuranceType
from src.models.country import Country
from src.services.base_service import BaseService
from src.services.exceptions import ValidationError, RelatedRecordsExistError


class ReinsurerService(BaseService):
    MAX_NAME = 100

    def _validate_create(self, db, **kwargs) -> dict:
        name = self.validate_company_name(kwargs.get("name"),"Nombre")

        self.validate_string_length(name,"Nombre",max_len=self.MAX_NAME)

        agency_id = kwargs.get("agency_id")
        if agency_id is None:
            raise ValidationError("La agencia es obligatoria.")
        self.get_or_404(db, Agency, agency_id, "Agencia")

        reinsurance_type_id = kwargs.get("reinsurance_type_id")
        if reinsurance_type_id is None:
            raise ValidationError("El tipo de reaseguro es obligatorio.")
        self.get_or_404(db, ReinsuranceType, reinsurance_type_id, "Tipo de Reaseguro")

        country_id = kwargs.get("country_id")
        if country_id is None:
            raise ValidationError("El país es obligatorio.")
        self.get_or_404(db, Country, country_id, "País")

        return dict(
            name=name, agency_id=agency_id,
            reinsurance_type_id=reinsurance_type_id, country_id=country_id,
        )

    def _validate_update(self, db, **kwargs) -> None:
        if "name" in kwargs:
            val = self.validate_company_name(kwargs["name"],"Nombre")
            self.validate_string_length(val,"Nombre",max_len=self.MAX_NAME)

            kwargs["name"] = val
        if "agency_id" in kwargs:
            self.get_or_404(db, Agency, kwargs["agency_id"], "Agencia")
        if "reinsurance_type_id" in kwargs:
            self.get_or_404(
                db, ReinsuranceType, kwargs["reinsurance_type_id"],
                "Tipo de Reaseguro"
            )
        if "country_id" in kwargs:
            self.get_or_404(db, Country, kwargs["country_id"], "País")

    def create(self, **kwargs):
        with get_db() as db:
            try:
                validated = self._validate_create(db, **kwargs)
                self.check_duplicate(db, Reinsurer, "name", validated["name"])
                kwargs_full = dict(kwargs)
                kwargs_full.update(validated)
                repo = ReinsurerRepository(db)
                instance = repo.create(**kwargs_full)
                db.commit()
                return instance
            except Exception:
                db.rollback()
                raise

    def get_by_id(self, reinsurer_id: int):
        with get_db() as db:
            repo = ReinsurerRepository(db)
            return repo.get_by_id(reinsurer_id)

    def get_all(self):
        with get_db() as db:
            return db.execute(
                select(Reinsurer).options(
                    joinedload(Reinsurer.agency),
                    joinedload(Reinsurer.reinsurance_type),
                    joinedload(Reinsurer.country),
                )
            ).scalars().all()

    def update(self, reinsurer_id: int, **kwargs):
        with get_db() as db:
            try:
                self.get_or_404(db, Reinsurer, reinsurer_id, "Reaseguradora")
                self._validate_update(db, **kwargs)
                if "name" in kwargs:
                    self.check_duplicate(
                        db, Reinsurer, "name",
                        kwargs["name"], exclude_id=reinsurer_id
                    )
                repo = ReinsurerRepository(db)
                instance = repo.update(reinsurer_id, **kwargs)
                db.commit()
                return instance
            except Exception:
                db.rollback()
                raise

    def delete(self, reinsurer_id: int):
        with get_db() as db:
            try:
                self.get_or_404(db, Reinsurer, reinsurer_id, "Reaseguradora")
                repo = ReinsurerRepository(db)
                result = repo.delete(reinsurer_id)
                db.commit()
                return result
            except IntegrityError:
                db.rollback()
                raise RelatedRecordsExistError(
                    "No se puede eliminar la reaseguradora porque tiene participaciones asociadas."
                )
            except Exception:
                db.rollback()
                raise
