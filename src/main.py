import sys
import os
import tkinter as tk

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.database.connection import engine, Base
from src.models import *  # noqa: F401, F403
from src.database.seed import seed_all
from src.ui.login_view import LoginView
from src.ui.home_view import HomeView
from src.ui.ui_scaling import UIScale


def main():
    Base.metadata.create_all(bind=engine)
    seed_all()

    root = tk.Tk()
    UIScale.initialize(root)
    root.withdraw()
    LoginView(root, on_success=lambda user: HomeView(root, user))
    root.mainloop()


if __name__ == "__main__":
    main()
