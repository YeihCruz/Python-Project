from sqlalchemy.exc import IntegrityError
from src.database.connection import get_db
from src.repositories.client_repository import ClientRepository
from src.models.client import Client
from src.models.agency import Agency
from src.models.gender import Gender
from src.models.country import Country
from src.services.base_service import BaseService
from src.services.exceptions import ValidationError, RelatedRecordsExistError


class ClientService(BaseService):
    MAX_FIRST_NAME = 80
    MAX_LAST_NAME = 100
    MAX_ID_NUMBER = 30
    MAX_ADDRESS = 200
    MAX_PHONE = 20
    MAX_EMAIL = 100
    MIN_AGE = 0
    MAX_AGE = 150

    def _validate_create(self, db, **kwargs) -> dict:
        value = self.validate_required(kwargs.get("first_name"), "Nombre")
        value = self.validate_only_letters(value, "Nombre")
        self.validate_string_length(value, "Nombre", max_len=self.MAX_FIRST_NAME)

        first_name = value

        value = self.validate_required(kwargs.get("last_name"), "Apellido")
        value = self.validate_only_letters(value, "Apellido")
        self.validate_string_length(value, "Apellido", max_len=self.MAX_LAST_NAME)

        last_name = value

        id_number = self.validate_required(
            kwargs.get("identification_number"), "Número de Identificación"
        )
        self.validate_string_length(
            id_number, "Número de Identificación", max_len=self.MAX_ID_NUMBER
        )

        age = kwargs.get("age")
        if age is None:
            raise ValidationError("La edad es obligatoria.")
        try:
            age_int = int(age)
        except (TypeError, ValueError):
            raise ValidationError("La edad debe ser un número entero.")
        if age_int < self.MIN_AGE or age_int > self.MAX_AGE:
            raise ValidationError(
                f"La edad debe estar entre {self.MIN_AGE} y {self.MAX_AGE} años."
            )

        address = self.validate_required(kwargs.get("address"), "Dirección")
        self.validate_string_length(address, "Dirección", max_len=self.MAX_ADDRESS)

        phone = self.validate_required(kwargs.get("phone"), "Teléfono")
        self.validate_string_length(phone, "Teléfono", max_len=self.MAX_PHONE)
        self.validate_phone(phone)

        email = self.validate_required(kwargs.get("email"), "Correo Electrónico")
        self.validate_string_length(email, "Correo Electrónico", max_len=self.MAX_EMAIL)
        self.validate_email(email)

        agency_id = kwargs.get("agency_id")
        if agency_id is None:
            raise ValidationError("La agencia es obligatoria.")
        self.get_or_404(db, Agency, agency_id, "Agencia")

        gender_id = kwargs.get("gender_id")
        if gender_id is None:
            raise ValidationError("El género es obligatorio.")
        self.get_or_404(db, Gender, gender_id, "Género")

        country_id = kwargs.get("country_id")
        if country_id is None:
            raise ValidationError("El país es obligatorio.")
        self.get_or_404(db, Country, country_id, "País")

        return dict(
            first_name=first_name, last_name=last_name,
            identification_number=id_number, age=age_int,
            address=address, phone=phone, email=email,
            agency_id=agency_id, gender_id=gender_id, country_id=country_id,
        )

    def _validate_update(self, db, **kwargs) -> None:
        if "first_name" in kwargs:
            val = self.validate_required(kwargs["first_name"], "Nombre")
            self.validate_string_length(val, "Nombre", max_len=self.MAX_FIRST_NAME)
        if "last_name" in kwargs:
            val = self.validate_required(kwargs["last_name"], "Apellido")
            self.validate_string_length(val, "Apellido", max_len=self.MAX_LAST_NAME)
        if "identification_number" in kwargs:
            val = self.validate_required(
                kwargs["identification_number"], "Número de Identificación"
            )
            self.validate_string_length(
                val, "Número de Identificación", max_len=self.MAX_ID_NUMBER
            )
        if "age" in kwargs:
            age = kwargs["age"]
            try:
                age_int = int(age)
            except (TypeError, ValueError):
                raise ValidationError("La edad debe ser un número entero.")
            if age_int < self.MIN_AGE or age_int > self.MAX_AGE:
                raise ValidationError(
                    f"La edad debe estar entre {self.MIN_AGE} y {self.MAX_AGE} años."
                )
        if "address" in kwargs:
            val = self.validate_required(kwargs["address"], "Dirección")
            self.validate_string_length(val, "Dirección", max_len=self.MAX_ADDRESS)
        if "phone" in kwargs:
            val = self.validate_required(kwargs["phone"], "Teléfono")
            self.validate_string_length(val, "Teléfono", max_len=self.MAX_PHONE)
            self.validate_phone(val)
        if "email" in kwargs:
            val = self.validate_required(kwargs["email"], "Correo Electrónico")
            self.validate_string_length(val, "Correo Electrónico", max_len=self.MAX_EMAIL)
            self.validate_email(val)
        if "agency_id" in kwargs:
            self.get_or_404(db, Agency, kwargs["agency_id"], "Agencia")
        if "gender_id" in kwargs:
            self.get_or_404(db, Gender, kwargs["gender_id"], "Género")
        if "country_id" in kwargs:
            self.get_or_404(db, Country, kwargs["country_id"], "País")

    def create(self, **kwargs):
        with get_db() as db:
            try:
                validated = self._validate_create(db, **kwargs)
                self.check_duplicate(
                    db, Client, "identification_number",
                    validated["identification_number"]
                )
                self.check_duplicate(db, Client, "email", validated["email"])
                repo = ClientRepository(db)
                instance = repo.create(**validated)
                db.commit()
                return instance
            except Exception:
                db.rollback()
                raise

    def get_by_id(self, client_id: int):
        with get_db() as db:
            repo = ClientRepository(db)
            return repo.get_by_id(client_id)

    def get_all(self):
        with get_db() as db:
            repo = ClientRepository(db)
            return repo.get_all()

    def update(self, client_id: int, **kwargs):
        with get_db() as db:
            try:
                self.get_or_404(db, Client, client_id, "Cliente")
                self._validate_update(db, **kwargs)
                if "identification_number" in kwargs:
                    self.check_duplicate(
                        db, Client, "identification_number",
                        kwargs["identification_number"], exclude_id=client_id
                    )
                if "email" in kwargs:
                    self.check_duplicate(
                        db, Client, "email",
                        kwargs["email"], exclude_id=client_id
                    )
                repo = ClientRepository(db)
                instance = repo.update(client_id, **kwargs)
                db.commit()
                return instance
            except Exception:
                db.rollback()
                raise

    def delete(self, client_id: int):
        with get_db() as db:
            try:
                self.get_or_404(db, Client, client_id, "Cliente")
                repo = ClientRepository(db)
                result = repo.delete(client_id)
                db.commit()
                return result
            except IntegrityError:
                db.rollback()
                raise RelatedRecordsExistError(
                    "No se puede eliminar el cliente porque tiene pólizas asociadas."
                )
            except Exception:
                db.rollback()
                raise
