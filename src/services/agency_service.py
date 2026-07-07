from sqlalchemy.exc import IntegrityError
from src.database.connection import get_db
from src.repositories.agency_repository import AgencyRepository
from src.models.agency import Agency
from src.services.base_service import BaseService
from src.services.exceptions import RelatedRecordsExistError


class AgencyService(BaseService):
    MAX_NAME = 100
    MAX_ADDRESS = 200
    MAX_PHONE = 20
    MAX_EMAIL = 100
    MAX_DIRECTOR = 100

    def _validate_create(self, **kwargs) -> dict:
        name = self.validate_company_name(
            self.validate_required(kwargs.get("name"), "Nombre"),
            "Nombre"
        )
        self.validate_string_length(name, "Nombre", max_len=self.MAX_NAME)

        address = self.validate_required(kwargs.get("address"), "Dirección")
        self.validate_string_length(address, "Dirección", max_len=self.MAX_ADDRESS)

        phone = self.validate_required(kwargs.get("phone"), "Teléfono")
        phone = phone.strip()
        self.validate_string_length(phone, "Teléfono", max_len=self.MAX_PHONE)
        self.validate_phone(phone)

        email = self.validate_required(kwargs.get("email"), "Correo Electrónico")
        email = email.strip().lower()
        self.validate_string_length(email, "Correo Electrónico", max_len=self.MAX_EMAIL)
        self.validate_email(email)

        general_director = self.validate_person_name(
            self.validate_required(kwargs.get("general_director"), "Director General"),
            "Director General"
        )
        self.validate_string_length(general_director, "Director General", max_len=self.MAX_DIRECTOR)

        insurance_manager = self.validate_person_name(
            self.validate_required(kwargs.get("insurance_manager"), "Gerente de Seguros"),
            "Gerente de Seguros"
        )
        self.validate_string_length(insurance_manager, "Gerente de Seguros", max_len=self.MAX_DIRECTOR)

        claims_manager = self.validate_person_name(
            self.validate_required(kwargs.get("claims_manager"), "Gerente de Reclamos"),
            "Gerente de Reclamos"
        )
        self.validate_string_length(claims_manager, "Gerente de Reclamos", max_len=self.MAX_DIRECTOR)

        return {
            "name": name,
            "address": address,
            "phone": phone,
            "email": email,
            "general_director": general_director,
            "insurance_manager": insurance_manager,
            "claims_manager": claims_manager,
        }

    def _validate_update(self, **kwargs) -> dict:
        data = {}

        if "name" in kwargs:
            name = self.validate_company_name(
                self.validate_required(kwargs["name"], "Nombre"),
                "Nombre"
            )
            self.validate_string_length(name, "Nombre", max_len=self.MAX_NAME)
            data["name"] = name

        if "address" in kwargs:
            address = self.validate_required(kwargs["address"], "Dirección")
            self.validate_string_length(address, "Dirección", max_len=self.MAX_ADDRESS)
            data["address"] = address

        if "phone" in kwargs:
            phone = self.validate_required(kwargs["phone"], "Teléfono").strip()
            self.validate_string_length(phone, "Teléfono", max_len=self.MAX_PHONE)
            self.validate_phone(phone)
            data["phone"] = phone

        if "email" in kwargs:
            email = self.validate_required(kwargs["email"], "Correo Electrónico").strip().lower()
            self.validate_string_length(email, "Correo Electrónico", max_len=self.MAX_EMAIL)
            self.validate_email(email)
            data["email"] = email

        if "general_director" in kwargs:
            val = self.validate_person_name(
                self.validate_required(
                    kwargs["general_director"],
                    "Director General"
                ),
                "Director General"
            )
            self.validate_string_length(val, "Director General", max_len=self.MAX_DIRECTOR)
            data["general_director"] = val

        if "insurance_manager" in kwargs:
            val = self.validate_person_name(
                self.validate_required(
                    kwargs["insurance_manager"],
                    "Gerente de Seguros"
                ),
                "Gerente de Seguros"
            )
            self.validate_string_length(val, "Gerente de Seguros", max_len=self.MAX_DIRECTOR)
            data["insurance_manager"] = val

        if "claims_manager" in kwargs:
            val = self.validate_person_name(
                self.validate_required(
                    kwargs["claims_manager"],
                    "Gerente de Reclamos"
                ),
                "Gerente de Reclamos"
            )
            self.validate_string_length(val, "Gerente de Reclamos", max_len=self.MAX_DIRECTOR)
            data["claims_manager"] = val

        return data

    def create(self, **kwargs):
        validated = self._validate_create(**kwargs)
        with get_db() as db:
            try:
                self.check_duplicate(db, Agency, "email", validated["email"])
                repo = AgencyRepository(db)
                instance = repo.create(**validated)
                db.commit()
                return instance
            except Exception:
                db.rollback()
                raise

    def update(self, agency_id: int, **kwargs):
        validated = self._validate_update(**kwargs)

        with get_db() as db:
            try:
                self.get_or_404(db, Agency, agency_id, "Agencia")

                if "email" in validated:
                    self.check_duplicate(
                        db, Agency, "email",
                        validated["email"],
                        exclude_id=agency_id
                    )

                repo = AgencyRepository(db)
                instance = repo.update(agency_id, **validated)
                db.commit()
                return instance

            except Exception:
                db.rollback()
                raise

    def get_by_id(self, agency_id: int):

     with get_db() as db:
              repo = AgencyRepository(db)
              return repo.get_by_id(agency_id)

    def get_all(self):
          with get_db() as db:
              repo = AgencyRepository(db)
              return repo.get_all()

    def delete(self, agency_id: int):
        with get_db() as db:
            try:
                self.get_or_404(db, Agency, agency_id, "Agencia")
                repo = AgencyRepository(db)
                result = repo.delete(agency_id)
                db.commit()
                return result

            except IntegrityError:
                db.rollback()
                raise RelatedRecordsExistError(
                    "No se puede eliminar la agencia porque tiene relaciones activas."
                )
            except Exception:
                db.rollback()
                raise