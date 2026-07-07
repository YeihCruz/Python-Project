from sqlalchemy.exc import IntegrityError
from src.database.connection import get_db
from src.repositories.reinsurance_participation_repository import ReinsuranceParticipationRepository
from src.models.reinsurance_participation import ReinsuranceParticipation
from src.models.reinsurer import Reinsurer
from src.models.insurance_type import InsuranceType
from src.services.base_service import BaseService
from src.services.exceptions import ValidationError, RelatedRecordsExistError


class ReinsuranceParticipationService(BaseService):
    MAX_PCT = 100

    def _validate_create(self, db, **kwargs) -> dict:
        reinsurer_id = kwargs.get("reinsurer_id")
        if reinsurer_id is None:
            raise ValidationError("La reaseguradora es obligatoria.")
        self.get_or_404(db, Reinsurer, reinsurer_id, "Reaseguradora")

        insurance_type_id = kwargs.get("insurance_type_id")
        if insurance_type_id is None:
            raise ValidationError("El tipo de seguro es obligatorio.")
        self.get_or_404(db, InsuranceType, insurance_type_id, "Tipo de Seguro")

        percentage = kwargs.get("participation_percentage")
        if percentage is None:
            raise ValidationError("El porcentaje de participación es obligatorio.")
        self.validate_min_max(percentage, "Porcentaje de Participación", min_val=0.01, max_val=self.MAX_PCT)

        return dict(
            reinsurer_id=reinsurer_id, insurance_type_id=insurance_type_id,
            participation_percentage=percentage,
        )

    def _validate_update(self, db, **kwargs) -> None:
        if "reinsurer_id" in kwargs:
            self.get_or_404(db, Reinsurer, kwargs["reinsurer_id"], "Reaseguradora")
        if "insurance_type_id" in kwargs:
            self.get_or_404(
                db, InsuranceType, kwargs["insurance_type_id"], "Tipo de Seguro"
            )
        if "participation_percentage" in kwargs:
            val = kwargs["participation_percentage"]
            if val is None:
                raise ValidationError("El porcentaje de participación es obligatorio.")
            self.validate_min_max(val, "Porcentaje de Participación", min_val=0.01, max_val=self.MAX_PCT)

    def create(self, **kwargs):
        with get_db() as db:
            try:
                validated = self._validate_create(db, **kwargs)
                self.check_duplicate_composite(
                    db, ReinsuranceParticipation,
                    {
                        "reinsurer_id": validated["reinsurer_id"],
                        "insurance_type_id": validated["insurance_type_id"],
                    }
                )
                kwargs_full = dict(kwargs)
                kwargs_full.update(validated)
                repo = ReinsuranceParticipationRepository(db)
                instance = repo.create(**kwargs_full)
                db.commit()
                return instance
            except Exception:
                db.rollback()
                raise

    def get_by_id(self, participation_id: int):
        with get_db() as db:
            repo = ReinsuranceParticipationRepository(db)
            return repo.get_by_id(participation_id)

    def get_all(self):
        with get_db() as db:
            repo = ReinsuranceParticipationRepository(db)
            return repo.get_all()

    def update(self, participation_id: int, **kwargs):
        with get_db() as db:
            try:
                self.get_or_404(
                    db, ReinsuranceParticipation, participation_id,
                    "Participación"
                )
                self._validate_update(db, **kwargs)
                repo = ReinsuranceParticipationRepository(db)
                reinsurer_id = kwargs.get(
                    "reinsurer_id",
                    repo.get_by_id(participation_id).reinsurer_id
                )
                insurance_type_id = kwargs.get(
                    "insurance_type_id",
                    repo.get_by_id(participation_id).insurance_type_id
                )
                self.check_duplicate_composite(
                    db, ReinsuranceParticipation,
                    {
                        "reinsurer_id": reinsurer_id,
                        "insurance_type_id": insurance_type_id,
                    },
                    exclude_id=participation_id,
                )
                instance = repo.update(participation_id, **kwargs)
                db.commit()
                return instance
            except Exception:
                db.rollback()
                raise

    def delete(self, participation_id: int):
        with get_db() as db:
            try:
                self.get_or_404(
                    db, ReinsuranceParticipation, participation_id,
                    "Participación"
                )
                repo = ReinsuranceParticipationRepository(db)
                result = repo.delete(participation_id)
                db.commit()
                return result
            except IntegrityError:
                db.rollback()
                raise RelatedRecordsExistError(
                    "No se puede eliminar la participación porque tiene registros asociados."
                )
            except Exception:
                db.rollback()
                raise
