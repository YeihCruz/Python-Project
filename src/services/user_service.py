import hashlib
from typing import Optional
from sqlalchemy.exc import IntegrityError
from src.database.connection import get_db
from src.repositories.user_repository import UserRepository
from src.models.user import User
from src.models.role import Role
from src.services.base_service import BaseService
from src.services.exceptions import ValidationError, RelatedRecordsExistError


class UserService(BaseService):
    MAX_USERNAME = 50
    MAX_PASSWORD = 255
    MAX_FULL_NAME = 100

    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def _validate_create(self, db, **kwargs) -> dict:
        role_id = kwargs.get("role_id")
        if role_id is None:
            raise ValidationError("El rol es obligatorio.")
        self.get_or_404(db, Role, role_id, "Rol")

        username = self.validate_username(kwargs.get("username"), "Usuario")
        self.validate_string_length(
            username, "Usuario", max_len=self.MAX_USERNAME
        )

        password = kwargs.get("password")
        if not password:
            raise ValidationError("La contraseña es obligatoria.")

        full_name = self.validate_required(
            kwargs.get("full_name"),
            "Nombre Completo"
        )

        full_name = self.validate_only_letters(
            full_name,
            "Nombre Completo"
        )

        self.validate_string_length(
            full_name,
            "Nombre Completo",
            max_len=self.MAX_FULL_NAME
        )

        return dict(
            role_id=role_id, username=username, password=password,
            full_name=full_name,
            active=kwargs.get("active", True),
        )

    def _validate_update(self, db, **kwargs) -> None:

        if "role_id" in kwargs:
            self.get_or_404(db, Role, kwargs["role_id"], "Rol")

        if "username" in kwargs:
            val = self.validate_username(kwargs["username"], "Usuario")
            self.validate_string_length(val, "Usuario", max_len=self.MAX_USERNAME)

        if "full_name" in kwargs:
            val = self.validate_required(
                kwargs["full_name"],
                "Nombre Completo"
            )

            val = self.validate_only_letters(
                val,
                "Nombre Completo"
            )

            self.validate_string_length(
                val,
                "Nombre Completo",
                max_len=self.MAX_FULL_NAME
            )

        if "active" in kwargs:
            kwargs["active"] = bool(kwargs["active"])

    def create(self, **kwargs):
        with get_db() as db:
            try:
                validated = self._validate_create(db, **kwargs)
                validated["password"] = self._hash_password(validated["password"])
                self.check_duplicate(db, User, "username", validated["username"])
                repo = UserRepository(db)
                instance = repo.create(**validated)
                db.commit()
                return instance
            except Exception:
                db.rollback()
                raise

    def get_by_id(self, user_id: int):
        with get_db() as db:
            repo = UserRepository(db)
            return repo.get_by_id(user_id)

    def get_all(self):
        with get_db() as db:
            repo = UserRepository(db)
            return repo.get_all()

    def update(self, user_id: int, **kwargs):
        with get_db() as db:
            try:
                self.get_or_404(db, User, user_id, "Usuario")
                self._validate_update(db, **kwargs)
                if "password" in kwargs:
                    kwargs["password"] = self._hash_password(kwargs["password"])
                if "username" in kwargs:
                    self.check_duplicate(
                        db, User, "username",
                        kwargs["username"], exclude_id=user_id
                    )
                repo = UserRepository(db)
                instance = repo.update(user_id, **kwargs)
                db.commit()
                return instance
            except Exception:
                db.rollback()
                raise

    def delete(self, user_id: int):
        with get_db() as db:
            try:
                self.get_or_404(db, User, user_id, "Usuario")

                repo = UserRepository(db)

                total_users = repo.count()

                if total_users <= 1:
                    raise ValidationError(
                        "Debe existir al menos un usuario en el sistema."
                    )

                result = repo.delete(user_id)

                db.commit()

                return result

            except IntegrityError:
                db.rollback()
                raise RelatedRecordsExistError(
                    "No se puede eliminar el usuario porque tiene registros asociados."
                )

            except Exception:
                db.rollback()
                raise

    def login(self, username: str, password: str) -> Optional[User]:
        hashed = self._hash_password(password)
        with get_db() as db:
            repo = UserRepository(db)
            user = repo.get_by_username(username)
            if user and user.password == hashed and user.active:
                return user
            return None

    def exists_admin(self) -> bool:
        with get_db() as db:
            repo = UserRepository(db)
            return repo.exists_admin()

    def deactivate(self, user_id: int):
        return self.update(user_id, active=False)
