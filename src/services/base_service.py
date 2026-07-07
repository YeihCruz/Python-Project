import re
from decimal import Decimal
from typing import Optional, Type, Any
from sqlalchemy import select
from sqlalchemy.orm import Session
from datetime import datetime

from src.services.exceptions import NotFoundError, ValidationError, DuplicateError


class BaseService:
    """Validaciones reutilizables para todas las capas de servicio."""

    @staticmethod
    def validate_only_letters(value: str, field_name: str) -> str:
        if value is None:
            raise ValidationError(f"{field_name} es obligatorio.")

        value = str(value).strip()

        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$", value):
            raise ValidationError(
                f"{field_name} solo puede contener letras."
            )

        return value

    @staticmethod
    def validate_description(value: str, field_name: str) -> str:
        value = BaseService.validate_required(value, field_name)

        if not re.match(
                r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$",
                value.strip()
        ):
            raise ValidationError(
                f"{field_name} solo puede contener letras."
            )

        return value.strip()

    @staticmethod
    def validate_person_name(value: str, field_name: str) -> str:
        if value is None:
            raise ValidationError(f"{field_name} es obligatorio.")

        value = str(value).strip()

        if not re.match(
                r"^[A-Za-zÁÉÍÓÚáéíóúÑñ.\s]+$",
                value
        ):
            raise ValidationError(
                f"{field_name} solo puede contener letras, espacios y puntos."
            )

        return value


    @staticmethod
    def validate_company_name(value: str, field_name: str) -> str:
        value = BaseService.validate_required(value, field_name)

        if not re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9&.,\-\s]+$", value):
            raise ValidationError(
                f"{field_name} contiene caracteres no válidos."
            )

        if value.isdigit():
            raise ValidationError(
                f"{field_name} no puede contener únicamente números."
            )

        return value

    @staticmethod
    def validate_username(value: str, field_name: str = "Usuario") -> str:
        value = BaseService.validate_required(value, field_name)

        # Solo letras, números y guiones bajos
        if not re.match(r"^[a-zA-Z0-9_.-]+$", value):
            raise ValidationError(
                f"{field_name} solo puede contener letras, números y guiones bajos."
            )

        # Debe contener al menos una letra
        if not re.search(r"[a-zA-Z]", value):
            raise ValidationError(
                f"{field_name} debe contener al menos una letra."
            )

        return value


    @staticmethod
    def validate_required(value: Any, field_name: str) -> str:
        if value is None or (isinstance(value, str) and not value.strip()):
            raise ValidationError(f"{field_name} es obligatorio.")
        return value.strip() if isinstance(value, str) else value

    @staticmethod
    def validate_string_length(
        value: str, field_name: str, min_len: int = 1, max_len: Optional[int] = None
    ) -> None:
        if not value:
            return
        stripped = value.strip() if isinstance(value, str) else str(value)
        if min_len and len(stripped) < min_len:
            raise ValidationError(
                f"{field_name} debe tener al menos {min_len} carácter(es)."
            )
        if max_len and len(stripped) > max_len:
            raise ValidationError(
                f"{field_name} no debe exceder {max_len} carácter(es)."
            )

    @staticmethod
    def validate_email(email: str) -> None:
        if not email:
            return
        pattern = r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, email.strip()):
            raise ValidationError(
                "El formato del correo electrónico no es válido."
            )

    @staticmethod
    def validate_phone(phone: str) -> None:
        if not phone:
            return
        cleaned = re.sub(r"[\s\+\-\(\)]", "", phone)
        if not cleaned.isdigit() or len(cleaned) < 5:
            raise ValidationError(
                "El teléfono debe contener al menos 5 dígitos."
            )

    @staticmethod
    def validate_date(value: Any, field_name: str):
        try:
            return datetime.strptime(
                str(value).strip(),
                "%Y-%m-%d"
            ).date()
        except Exception:
            raise ValidationError(
                f"{field_name} debe tener formato YYYY-MM-DD."
            )

    @staticmethod
    def validate_positive_number(value: Any, field_name: str) -> None:
        if value is None:
            return
        try:
            val = Decimal(str(value))
            if val <= 0:
                raise ValidationError(f"{field_name} debe ser mayor que cero.")
        except (TypeError, ValueError, ArithmeticError):
            raise ValidationError(f"{field_name} debe ser un valor numérico válido.")

    @staticmethod
    def validate_max_number(value, field_name, max_value):
        if value is None:
            return

        try:
            val = Decimal(str(value))

            if val > Decimal(str(max_value)):
                raise ValidationError(
                    f"{field_name} no puede ser mayor que {max_value}."
                )

        except Exception:
            raise ValidationError(
                f"{field_name} debe ser un número válido."
            )

    @staticmethod
    def validate_min_max(
        value: Any, field_name: str, min_val: Optional[float] = None, max_val: Optional[float] = None
    ) -> None:
        if value is None:
            return
        try:
            val = Decimal(str(value))
            if min_val is not None and val < Decimal(str(min_val)):
                raise ValidationError(
                    f"{field_name} debe ser mayor o igual que {min_val}."
                )
            if max_val is not None and val > Decimal(str(max_val)):
                raise ValidationError(
                    f"{field_name} debe ser menor o igual que {max_val}."
                )
        except (TypeError, ValueError, ArithmeticError):
            raise ValidationError(f"{field_name} debe ser un valor numérico válido.")

    @staticmethod
    def validate_text_not_numeric(value, field_name):
            if not value:
                return value

            value = str(value).strip()

            if value.isdigit():
                raise ValidationError(
                    f"{field_name} no puede contener únicamente números."
                )

            return value

    @staticmethod
    def validate_reason_text(value, field_name):

        value = BaseService.validate_required(value,field_name)

        value = str(value).strip()

        if value.isdigit():
            raise ValidationError(
                f"{field_name} no puede contener únicamente números."
            )

        if not re.match(
                r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9\s,.;:()\-]+$",
                value
        ):
            raise ValidationError(
                f"{field_name} contiene caracteres no permitidos."
            )

        return value

    @staticmethod
    def check_duplicate(
        session: Session,
        model_class: Type,
        field: str,
        value: Any,
        exclude_id: Optional[int] = None,
    ) -> None:
        if not value:
            return
        pk_name = list(model_class.__table__.primary_key.columns.keys())[0]
        query = select(model_class).where(
            getattr(model_class, field) == value
        )
        if exclude_id is not None:
            query = query.where(
                getattr(model_class, pk_name) != exclude_id
            )
        existing = session.execute(query).scalar_one_or_none()
        if existing:
            msg = f"Ya existe un registro con '{field}' = '{value}'."
            raise DuplicateError(msg)

    @staticmethod
    def check_duplicate_composite(
        session: Session,
        model_class: Type,
        filters: dict,
        exclude_id: Optional[int] = None,
    ) -> None:
        pk_name = list(model_class.__table__.primary_key.columns.keys())[0]
        query = select(model_class)
        for field, value in filters.items():
            query = query.where(getattr(model_class, field) == value)
        if exclude_id is not None:
            query = query.where(getattr(model_class, pk_name) != exclude_id)
        existing = session.execute(query).scalar_one_or_none()
        if existing:
            parts = [f"'{v}'" for v in filters.values()]
            msg = f"Ya existe un registro con los valores {', '.join(parts)}."
            raise DuplicateError(msg)

    @staticmethod
    def get_or_404(
        session: Session, model_class: Type, id_value: int, field_name: str = "ID"
    ) -> Any:
        instance = session.get(model_class, id_value)
        if instance is None:
            raise NotFoundError(
                f"{field_name} con ID '{id_value}' no encontrado."
            )
        return instance

    @staticmethod
    def validate_date_range(start_date: Any, end_date: Any) -> None:

        try:
            start = datetime.strptime(
                str(start_date).strip(),
                "%Y-%m-%d"
            ).date()
        except Exception:
            raise ValidationError(
                "La fecha de inicio debe tener formato YYYY-MM-DD."
            )

        try:
            end = datetime.strptime(
                str(end_date).strip(),
                "%Y-%m-%d"
            ).date()
        except Exception:
            raise ValidationError(
                "La fecha de fin debe tener formato YYYY-MM-DD."
            )

        if end <= start:
            raise ValidationError(
                "La fecha de fin debe ser posterior a la fecha de inicio."
            )




