from src.models.user import User


class SessionManager:
    _current_user: User = None

    @classmethod
    def login(cls, user: User):
        cls._current_user = user

    @classmethod
    def logout(cls):
        cls._current_user = None

    @classmethod
    def get_current_user(cls):
        return cls._current_user

    @classmethod
    def is_authenticated(cls) -> bool:
        return cls._current_user is not None
