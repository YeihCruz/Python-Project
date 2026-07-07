from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from src.database.connection import get_db
from src.repositories.claim_repository import ClaimRepository
from src.models.claim import Claim
from src.models.policy import Policy
from src.models.claim_type import ClaimType
from src.models.claim_status import ClaimStatus
from src.services.base_service import BaseService
from src.services.exceptions import ValidationError, RelatedRecordsExistError
from sqlalchemy.orm import joinedload

class ClaimService(BaseService):

    def _validate_create(self, db, **kwargs) -> dict:
        policy_number = kwargs.get("policy_number")
        if policy_number is None:
            raise ValidationError("La póliza es obligatoria.")
        self.get_or_404(db, Policy, policy_number, "Póliza")

        claim_type_id = kwargs.get("claim_type_id")
        if claim_type_id is None:
            raise ValidationError("El tipo de reclamo es obligatorio.")
        self.get_or_404(db, ClaimType, claim_type_id, "Tipo de Reclamo")

        claim_status_id = kwargs.get("claim_status_id")
        if claim_status_id is None:
            raise ValidationError("El estado del reclamo es obligatorio.")
        self.get_or_404(db, ClaimStatus, claim_status_id, "Estado de Reclamo")

        incident_date = self.validate_required(kwargs.get("incident_date"),"Fecha del Incidente")

        incident_date = self.validate_date(incident_date,"Fecha del Incidente")

        claimed_amount = self.validate_required(kwargs.get("claimed_amount"), "Monto Reclamado")

        self.validate_positive_number(claimed_amount,"Monto Reclamado")

        self.validate_max_number(claimed_amount,"Monto Reclamado",9999999999.99)

        compensated_amount = kwargs.get("compensated_amount")

        if compensated_amount not in (None, ""):
            self.validate_min_max( compensated_amount, "Monto Compensado",min_val=0)

            self.validate_max_number(compensated_amount,"Monto Compensado",9999999999.99)

        rejection_reason = kwargs.get("rejection_reason")

        if claim_status_id == 4:
            if rejection_reason in (None, ""):
                raise ValidationError("Motivo de Rechazo es obligatorio para reclamos rechazados.")
            rejection_reason = self.validate_reason_text(rejection_reason,"Motivo de Rechazo")
            self.validate_string_length(rejection_reason,"Motivo de Rechazo",max_len=255)
        elif rejection_reason not in (None, ""):
            rejection_reason = self.validate_reason_text(rejection_reason,"Motivo de Rechazo")
            self.validate_string_length(rejection_reason,"Motivo de Rechazo",max_len=255)

        return dict(
            policy_number=policy_number,
            claim_type_id=claim_type_id,
            claim_status_id=claim_status_id,
            incident_date=incident_date,
            claimed_amount=claimed_amount,
            compensated_amount=compensated_amount,
            rejection_reason=rejection_reason,
        )

    def _validate_update(self, db, **kwargs) -> None:

        if "policy_number" in kwargs:
            self.get_or_404(db,Policy,kwargs["policy_number"],"Póliza")

        if "claim_type_id" in kwargs:
            self.get_or_404(db,ClaimType,kwargs["claim_type_id"],"Tipo de Reclamo")

        if "claim_status_id" in kwargs:
            self.get_or_404(db,ClaimStatus,kwargs["claim_status_id"],"Estado de Reclamo")

        if "incident_date" in kwargs:
            kwargs["incident_date"] = self.validate_date(kwargs["incident_date"],"Fecha del Incidente")

        if "claimed_amount" in kwargs:
            self.validate_positive_number(kwargs["claimed_amount"],"Monto Reclamado")
            self.validate_max_number(kwargs["claimed_amount"],"Monto Reclamado",9999999999.99)

        if "compensated_amount" in kwargs:
            val = kwargs["compensated_amount"]

            if val not in (None, ""):
                self.validate_min_max(val,"Monto Compensado",min_val=0)
                self.validate_max_number(val,"Monto Compensado",9999999999.99)

        if "rejection_reason" in kwargs:
            kwargs["rejection_reason"] = self.validate_reason_text(kwargs["rejection_reason"],"Motivo de Rechazo")

            self.validate_string_length(kwargs["rejection_reason"],"Motivo de Rechazo",max_len=255)

    def create(self, **kwargs):
        with get_db() as db:
            try:
                validated = self._validate_create(db, **kwargs)
                kwargs_full = dict(kwargs)
                kwargs_full.update(validated)
                repo = ClaimRepository(db)
                instance = repo.create(**kwargs_full)
                db.commit()
                return instance
            except Exception:
                db.rollback()
                raise

    def get_by_id(self, claim_number: int):
        with get_db() as db:
            repo = ClaimRepository(db)
            return repo.get_by_id(claim_number)

    def get_all(self):
        with get_db() as db:
            result = db.execute(
                select(
                    Claim.claim_number,
                    Claim.policy_number,
                    Claim.claim_type_id,
                    Claim.claim_status_id,
                    Claim.incident_date,
                    Claim.claimed_amount,
                    Claim.compensated_amount,
                    Claim.rejection_reason,
                    Policy,
                    ClaimType,
                    ClaimStatus
                )
                .join(Policy, Claim.policy_number == Policy.policy_number)
                .join(ClaimType, Claim.claim_type_id == ClaimType.claim_type_id)
                .join(ClaimStatus, Claim.claim_status_id == ClaimStatus.claim_status_id)
            ).all()

            return result

    def update(self, claim_number: int, **kwargs):
        with get_db() as db:
            try:
                self.get_or_404(db, Claim, claim_number, "Reclamo")
                self._validate_update(db, **kwargs)
                repo = ClaimRepository(db)
                instance = repo.update(claim_number, **kwargs)
                db.commit()
                return instance
            except Exception:
                db.rollback()
                raise

    def delete(self, claim_number: int):
        with get_db() as db:
            try:
                self.get_or_404(db, Claim, claim_number, "Reclamo")
                repo = ClaimRepository(db)
                result = repo.delete(claim_number)
                db.commit()
                return result
            except IntegrityError:
                db.rollback()
                raise RelatedRecordsExistError(
                    "No se puede eliminar el reclamo porque tiene registros asociados."
                )
            except Exception:
                db.rollback()
                raise
