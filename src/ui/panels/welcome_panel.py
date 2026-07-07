import tkinter as tk
from src.ui.ui_styles import UIStyles
from src.ui.session_manager import SessionManager
from src.ui.ui_scaling import UIScale


class WelcomePanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=UIStyles.BG_LIGHT)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        center = tk.Frame(self, bg=UIStyles.BG_LIGHT)
        center.grid(row=0, column=0)

        user = SessionManager.get_current_user()
        tk.Label(center, text="Bienvenido a su Sistema de Gestión de Seguros",
                 font=("Segoe UI", UIScale.font(26), "bold"),
                 fg=UIStyles.TEXT_PRIMARY, bg=UIStyles.BG_LIGHT).pack()
        if user:
            tk.Label(center, text=f"Usuario: {user.username}",
                     font=("Segoe UI", UIScale.font(15)),
                     fg=UIStyles.TEXT_SECONDARY, bg=UIStyles.BG_LIGHT
                     ).pack(pady=UIScale.px(10))
