import tkinter as tk
from tkinter import ttk, messagebox
from src.models.user import User
from src.ui.ui_styles import UIStyles
from src.ui.session_manager import SessionManager
from src.ui.panels.welcome_panel import WelcomePanel
from src.ui.panels.users_panel import UsersPanel
from src.ui.panels.clients_panel import ClientsPanel
from src.ui.panels.policies_panel import PoliciesPanel
from src.ui.panels.claims_panel import ClaimsPanel
from src.ui.panels.reinsurers_panel import ReinsurersPanel
from src.ui.panels.agency_panel import AgencyPanel
from src.ui.panels.reports_panel import ReportsPanel


class HomeView(tk.Toplevel):
    def __init__(self, user: User):
        super().__init__()
        self.user = user
        SessionManager.login(user)

        self.title("Sistema de Seguros")
        self.state("zoomed")
        self.configure(bg=UIStyles.BG_LIGHT)

        self._panels = {}
        self._current_panel = None

        self._build_ui()

    def _build_ui(self):
        self._create_header()
        self._create_main_area()
        self._create_navigation()

    def _create_header(self):
        header = tk.Frame(self, bg=UIStyles.CARD_BG, height=50)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        self.header_title = tk.Label(header, text="Inicio",
                                     font=("Segoe UI", 16, "bold"),
                                     fg=UIStyles.TEXT_PRIMARY, bg=UIStyles.CARD_BG)
        self.header_title.pack(side="left", padx=20)

        user_info = tk.Frame(header, bg=UIStyles.CARD_BG)
        user_info.pack(side="right", padx=20)

        tk.Label(user_info, text="👤", font=("Segoe UI", 14),
                 bg=UIStyles.CARD_BG).pack(side="left")
        tk.Label(user_info, text=self.user.username,
                 font=("Segoe UI", 11),
                 fg=UIStyles.TEXT_PRIMARY, bg=UIStyles.CARD_BG).pack(side="left", padx=5)

        btn_logout = tk.Button(header, text="🚪  Cerrar Sesión",
                               font=("Segoe UI", 10),
                               fg="#C87878", bg=UIStyles.CARD_BG,
                               relief="flat", command=self._logout)
        btn_logout.pack(side="right", padx=(0, 20))
        self._bind_hover(btn_logout, lambda: btn_logout.configure(bg="#F0F0F0"),
                         lambda: btn_logout.configure(bg=UIStyles.CARD_BG))

    def _create_main_area(self):
        self.main_container = tk.Frame(self, bg=UIStyles.BG_LIGHT)
        self.main_container.pack(fill="both", expand=True)

    def _create_navigation(self):
        nav_buttons = [
            ("Inicio", 0),
            ("Usuarios", 1),
            ("Clientes", 2),
            ("Pólizas", 3),
            ("Reclamos", 4),
            ("Reaseguradoras", 5),
            ("Agencia", 6),
            ("Reportes", 7),
        ]
        self._nav_btns = []

        def show_panel(index):
            panel_map = {
                0: ("welcome", WelcomePanel),
                1: ("users", UsersPanel),
                2: ("clients", ClientsPanel),
                3: ("policies", PoliciesPanel),
                4: ("claims", ClaimsPanel),
                5: ("reinsurers", ReinsurersPanel),
                6: ("agency", AgencyPanel),
                7: ("reports", ReportsPanel),
            }
            key, panel_class = panel_map[index]

            if self._current_panel is not None:
                self._current_panel.pack_forget()

            if key not in self._panels:
                panel = panel_class(self.main_container)
                self._panels[key] = panel
            else:
                panel = self._panels[key]

            panel.pack(fill="both", expand=True)
            self._current_panel = panel
            self.header_title.configure(text=nav_buttons[index][0])

        welcome = WelcomePanel(self.main_container)
        welcome.pack(fill="both", expand=True)
        self._current_panel = welcome
        self._panels["welcome"] = welcome

    def _bind_hover(self, widget, enter_cmd, leave_cmd):
        widget.bind("<Enter>", lambda e: enter_cmd())
        widget.bind("<Leave>", lambda e: leave_cmd())

    def _logout(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Está seguro de que desea cerrar sesión?"):
            SessionManager.logout()
            self.destroy()

    def run(self):
        self.mainloop()
