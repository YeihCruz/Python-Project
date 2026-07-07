from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from src.database.connection import get_db
from src.repositories.policy_repository import PolicyRepository
from src.models.policy import Policy
from src.models.client import Client
from src.models.insurance_type import InsuranceType
from src.models.policy_status import PolicyStatus
from src.services.base_service import BaseService
from src.services.exceptions import ValidationError, RelatedRecordsExistError


class PolicyService(BaseService):

    def _validate_create(self, db, **kwargs) -> dict:
        client_id = kwargs.get("client_id")
        if client_id is None:
            raise ValidationError("El cliente es obligatorio.")
        self.get_or_404(db, Client, client_id, "Cliente")

        insurance_type_id = kwargs.get("insurance_type_id")
        if insurance_type_id is None:
            raise ValidationError("El tipo de seguro es obligatorio.")
        self.get_or_404(db, InsuranceType, insurance_type_id, "Tipo de Seguro")

        policy_status_id = kwargs.get("policy_status_id")
        if policy_status_id is None:
            raise ValidationError("El estado de póliza es obligatorio.")
        self.get_or_404(db, PolicyStatus, policy_status_id, "Estado de Póliza")

        start_date = self.validate_required(kwargs.get("start_date"),"Fecha de inicio")

        end_date = self.validate_required(kwargs.get("end_date"),"Fecha de fin")

        start_date = self.validate_date(start_date, "Fecha de inicio")
        end_date = self.validate_date(end_date, "Fecha de fin")

        self.validate_date_range(start_date, end_date)

        monthly_premium = self.validate_required(kwargs.get("monthly_premium"),"Prima Mensual")
        self.validate_positive_number(monthly_premium, "Prima Mensual")
        self.validate_max_number(monthly_premium,"Prima Mensual",9999999999.99)

        insured_amount = self.validate_required(kwargs.get("insured_amount"), "Monto Asegurado")
        self.validate_positive_number(insured_amount, "Monto Asegurado")
        self.validate_max_number(insured_amount,"Monto Asegurado",9999999999.99)

        cancellation_reason = kwargs.get("cancellation_reason")

        if cancellation_reason:
            cancellation_reason = self.validate_text_not_numeric(
                cancellation_reason,
                "Motivo de Cancelación"
            )

        return dict(
            client_id=client_id,
            insurance_type_id=insurance_type_id,
            policy_status_id=policy_status_id,
            start_date=start_date,
            end_date=end_date,
            monthly_premium=monthly_premium,
            insured_amount=insured_amount,
            cancellation_reason=cancellation_reason
        )

    def _validate_update(self, db, **kwargs) -> None:
        if "client_id" in kwargs:
            self.get_or_404(db, Client, kwargs["client_id"], "Cliente")
        if "insurance_type_id" in kwargs:
            self.get_or_404(db, InsuranceType, kwargs["insurance_type_id"], "Tipo de Seguro")
        if "policy_status_id" in kwargs:
            self.get_or_404(db, PolicyStatus, kwargs["policy_status_id"], "Estado de Póliza")
        if "start_date" in kwargs:
            kwargs["start_date"] = self.validate_date(kwargs["start_date"],"Fecha de Inicio")

        if "end_date" in kwargs:
            kwargs["end_date"] = self.validate_date(kwargs["end_date"],"Fecha de Fin")
        if "start_date" in kwargs and "end_date" in kwargs:
            self.validate_date_range(kwargs["start_date"], kwargs["end_date"])
        if "monthly_premium" in kwargs:
            self.validate_positive_number(kwargs["monthly_premium"], "Prima Mensual")
        if "insured_amount" in kwargs:
            self.validate_positive_number(kwargs["insured_amount"], "Monto Asegurado")
        if "cancellation_reason" in kwargs and kwargs["cancellation_reason"]:
                kwargs["cancellation_reason"] = self.validate_text_not_numeric(
                    kwargs["cancellation_reason"],"Motivo de Cancelación")

    def create(self, **kwargs):
        with get_db() as db:
            try:
                validated = self._validate_create(db, **kwargs)
                kwargs_full = dict(kwargs)
                kwargs_full.update(validated)
                repo = PolicyRepository(db)
                instance = repo.create(**kwargs_full)
                db.commit()
                return instance
            except Exception:
                db.rollback()
                raise

    def get_by_id(self, policy_number: int):
        with get_db() as db:
            repo = PolicyRepository(db)
            return repo.get_by_id(policy_number)

    def get_all(self):
        with get_db() as db:
            return db.execute(
                select(Policy).options(
                    joinedload(Policy.client),
                    joinedload(Policy.insurance_type),
                    joinedload(Policy.policy_status),
                )
            ).scalars().all()

    def update(self, policy_number: int, **kwargs):
        with get_db() as db:
            try:
                self.get_or_404(db, Policy, policy_number, "Póliza")
                self._validate_update(db, **kwargs)
                repo = PolicyRepository(db)
                instance = repo.update(policy_number, **kwargs)
                db.commit()
                return instance
            except Exception:
                db.rollback()
                raise

    def delete(self, policy_number: int):
        with get_db() as db:
            try:
                self.get_or_404(db, Policy, policy_number, "Póliza")
                repo = PolicyRepository(db)
                result = repo.delete(policy_number)
                db.commit()
                return result
            except IntegrityError:
                db.rollback()
                raise RelatedRecordsExistError(
                    "No se puede eliminar la póliza porque tiene coberturas o reclamos asociados."
                )
            except Exception:
                db.rollback()
                raise
