import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.database.connection import engine, Base
from src.models import *  # noqa: F401, F403
from src.services.user_service import UserService
from src.services.role_service import RoleService
from src.ui.login_view import LoginView


def seed_default_data():
    role_svc = RoleService()
    if not role_svc.get_by_id(1):
        role_svc.create(role_id=1, name="admin")
        print("Default role created.")

    user_svc = UserService()
    if user_svc.exists_admin():
        print("Admin already exists.")
        return
    print("No admin found. Creating default admin...")
    user_svc.create(
        role_id=1,
        username="admin",
        password="admin",
        full_name="System Administrator",
        active=True,
    )
    print("Default admin created:")
    print("username: admin")
    print("password: admin")


def main():
    Base.metadata.create_all(bind=engine)
    seed_default_data()
    app = LoginView()
    app.mainloop()


if __name__ == "__main__":
    main()
