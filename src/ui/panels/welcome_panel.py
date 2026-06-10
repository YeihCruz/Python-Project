import tkinter as tk
from src.ui.ui_styles import UIStyles
from src.ui.session_manager import SessionManager


class WelcomePanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=UIStyles.BG_LIGHT)
        user = SessionManager.get_current_user()
        welcome_text = f"Bienvenido, {user.full_name if user else 'Usuario'}"
        tk.Label(self, text=welcome_text,
                 font=("Segoe UI", 24, "bold"),
                 fg=UIStyles.TEXT_PRIMARY, bg=UIStyles.BG_LIGHT).pack(expand=True)
        tk.Label(self, text="Sistema de Gestión de Seguros",
                 font=("Segoe UI", 14),
                 fg=UIStyles.TEXT_SECONDARY, bg=UIStyles.BG_LIGHT).pack()
