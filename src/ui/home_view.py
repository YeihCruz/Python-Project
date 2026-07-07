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
from src.ui.panels.nomenclators_panel import NomenclatorsPanel
from src.ui.login_view import LoginView
from src.ui.ui_scaling import UIScale


class HomeView(tk.Toplevel):
    def __init__(self, master, user: User):
        super().__init__(master)
        self.user = user
        SessionManager.login(user)

        self.title("Sistema de Seguros")
        self.state("zoomed")
        self.configure(bg=UIStyles.BG_LIGHT)

        self._panels = {}
        self._current_panel = None

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_ui(self):
        self._create_header()
        self._create_main_area()
        self._create_navigation()
        self.bind("<Configure>", self._on_root_resize)

    def _create_header(self):
        h = UIScale.px(56)
        self.header = tk.Frame(self, bg=UIStyles.CARD_BG, height=h)
        self.header.pack(fill="x", side="top")
        self.header.pack_propagate(False)

        self.header_title = tk.Label(self.header, text="Inicio",
                                     font=("Segoe UI", UIScale.font(16), "bold"),
                                     fg=UIStyles.TEXT_PRIMARY, bg=UIStyles.CARD_BG)
        self.header_title.pack(side="left", padx=UIScale.px(20))

        user_info = tk.Frame(self.header, bg=UIStyles.CARD_BG)
        user_info.pack(side="right", padx=UIScale.px(20))

        tk.Label(user_info, text="👤", font=("Segoe UI", UIScale.font(14)),
                 bg=UIStyles.CARD_BG).pack(side="left")
        tk.Label(user_info, text=self.user.username,
                 font=("Segoe UI", UIScale.font(11)),
                 fg=UIStyles.TEXT_PRIMARY, bg=UIStyles.CARD_BG
                 ).pack(side="left", padx=UIScale.px(5))

        self.btn_logout = tk.Button(self.header, text="🚪  Cerrar Sesión",
                                    font=("Segoe UI", UIScale.font(10)),
                                    fg="#C87878", bg=UIStyles.CARD_BG,
                                    relief="flat", command=self._logout)
        self.btn_logout.pack(side="right", padx=(0, UIScale.px(20)))
        self._bind_hover(self.btn_logout,
                         lambda: self.btn_logout.configure(bg="#F0F0F0"),
                         lambda: self.btn_logout.configure(bg=UIStyles.CARD_BG))

    def _create_main_area(self):
        self.body = tk.Frame(self, bg=UIStyles.BG_LIGHT)
        self.body.pack(fill="both", expand=True)

        self.sidebar = tk.Frame(self.body, bg=UIStyles.SIDEBAR_BG)
        self.sidebar.pack(side="left", fill="y")

        self.main_container = tk.Frame(self.body, bg=UIStyles.BG_LIGHT)
        self.main_container.pack(fill="both", expand=True)

    def _on_root_resize(self, event):
        if event.widget is not self:
            return
        sw = max(UIScale.px(180), min(UIScale.px(320), int(event.width * 0.16)))
        self.sidebar.configure(width=sw)

    def _create_navigation(self):
        nav_buttons = [
            ("🏠  Inicio", 0),
            ("👥  Usuarios", 1),
            ("👤  Clientes", 2),
            ("📄  Pólizas", 3),
            ("⚠️   Reclamos", 4),
            ("🏢  Reaseguradoras", 5),
            ("🏛️   Agencia", 6),
            ("📋  Catálogos del Sistema", 7),
            ("📊  Reportes", 8),
        ]
        self._nav_btns = []
        self._current_nav_index = 0

        panel_map = {
            0: ("welcome", WelcomePanel),
            1: ("users", UsersPanel),
            2: ("clients", ClientsPanel),
            3: ("policies", PoliciesPanel),
            4: ("claims", ClaimsPanel),
            5: ("reinsurers", ReinsurersPanel),
            6: ("agency", AgencyPanel),
            7: ("nomenclators", NomenclatorsPanel),
            8: ("reports", ReportsPanel),
        }

        def show_panel(index):
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
            self._current_nav_index = index
            self._update_nav_highlight()
            label = nav_buttons[index][0]
            if "  " in label:
                label = label.split("  ", 1)[1]
            self.header_title.configure(text=label)

        for text, index in nav_buttons:
            btn = tk.Button(self.sidebar, text=text,
                            font=("Segoe UI", UIScale.font(11)),
                            bg=UIStyles.SIDEBAR_BG, fg=UIStyles.SIDEBAR_TEXT,
                            bd=0, relief="flat",
                            anchor="w", padx=UIScale.px(20), pady=UIScale.px(12),
                            cursor="hand2",
                            command=lambda i=index: show_panel(i))
            btn.pack(fill="x")
            self._nav_btns.append(btn)

        self._update_nav_highlight()

        welcome = WelcomePanel(self.main_container)
        welcome.pack(fill="both", expand=True)
        self._current_panel = welcome
        self._panels["welcome"] = welcome

    def _update_nav_highlight(self):
        for i, btn in enumerate(self._nav_btns):
            if i == self._current_nav_index:
                btn.configure(bg=UIStyles.SIDEBAR_SELECTED, fg="white")
            else:
                btn.configure(bg=UIStyles.SIDEBAR_BG, fg=UIStyles.SIDEBAR_TEXT)

    def _bind_hover(self, widget, enter_cmd, leave_cmd):
        widget.bind("<Enter>", lambda e: enter_cmd())
        widget.bind("<Leave>", lambda e: leave_cmd())

    def _logout(self):
        if messagebox.askyesno("Cerrar Sesión",
                               "¿Está seguro de que desea cerrar sesión?"):
            SessionManager.logout()
            self.destroy()
            LoginView(self.master, on_success=lambda user: HomeView(self.master, user))

    def _on_close(self):
        self.master.destroy()
