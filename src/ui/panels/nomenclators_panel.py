import tkinter as tk
from src.ui.ui_styles import UIStyles
from src.ui.components.simple_catalog_panel import SimpleCatalogPanel
from src.services.claim_status_service import ClaimStatusService
from src.services.claim_type_service import ClaimTypeService
from src.services.country_service import CountryService
from src.services.gender_service import GenderService
from src.services.insurance_type_service import InsuranceTypeService
from src.services.policy_status_service import PolicyStatusService
from src.services.reinsurance_type_service import ReinsuranceTypeService
from src.ui.ui_scaling import UIScale

ISO_CODES = [
    "AF", "AL", "DZ", "AD", "AO", "AR", "AM", "AU", "AT", "AZ",
    "BS", "BH", "BD", "BB", "BY", "BE", "BZ", "BJ", "BO", "BA",
    "BW", "BR", "BN", "BG", "BF", "BI", "CV", "KH", "CM", "CA",
    "CF", "TD", "CL", "CN", "CO", "KM", "CG", "CD", "CR", "HR",
    "CU", "CY", "CZ", "DK", "DJ", "DM", "DO", "EC", "EG", "SV",
    "GQ", "ER", "EE", "SZ", "ET", "FJ", "FI", "FR", "GA", "GM",
    "GE", "DE", "GH", "GR", "GT", "GN", "GW", "GY", "HT", "HN",
    "HU", "IS", "IN", "ID", "IR", "IQ", "IE", "IL", "IT", "CI",
    "JM", "JP", "JO", "KZ", "KE", "KI", "KP", "KR", "KW", "KG",
    "LA", "LV", "LB", "LS", "LR", "LY", "LI", "LT", "LU", "MG",
    "MW", "MY", "MV", "ML", "MT", "MH", "MR", "MU", "MX", "FM",
    "MD", "MC", "MN", "ME", "MA", "MZ", "MM", "NA", "NR", "NP",
    "NL", "NZ", "NI", "NE", "NG", "MK", "NO", "OM", "PK", "PW",
    "PA", "PG", "PY", "PE", "PH", "PL", "PT", "QA", "RO", "RU",
    "RW", "KN", "LC", "VC", "WS", "SM", "ST", "SA", "SN", "RS",
    "SC", "SL", "SG", "SK", "SI", "SB", "SO", "ZA", "SS", "ES",
    "LK", "SD", "SR", "SE", "CH", "SY", "TW", "TJ", "TZ", "TH",
    "TL", "TG", "TO", "TT", "TN", "TR", "TM", "TV", "UG", "UA",
    "AE", "GB", "US", "UY", "UZ", "VU", "VA", "VE", "VN", "YE",
    "ZM", "ZW",
]

NOMENCLATORS = [
    {
        "title": "Estados de Reclamo",
        "icon": "🔵",
        "color": UIStyles.CARD_BLUE,
        "service_cls": ClaimStatusService,
        "fields": [("Descripción:", "description")],
        "columns": [("description", "Descripción", 250)],
        "id_attr": "claim_status_id",
    },
    {
        "title": "Tipos de Reclamo",
        "icon": "🟡",
        "color": UIStyles.CARD_ORANGE,
        "service_cls": ClaimTypeService,
        "fields": [("Descripción:", "description")],
        "columns": [("description", "Descripción", 250)],
        "id_attr": "claim_type_id",
    },
    {
        "title": "Países",
        "icon": "🌍",
        "color": UIStyles.CARD_TEAL,
        "service_cls": CountryService,
        "fields": [("Nombre:", "name"), ("Código ISO:", "iso_code")],
        "columns": [("name", "Nombre", 200), ("iso_code", "ISO", 80)],
        "id_attr": "country_id",
        "combo_fields": {"iso_code": ISO_CODES},
    },
    {
        "title": "Géneros",
        "icon": "👤",
        "color": UIStyles.CARD_PURPLE,
        "service_cls": GenderService,
        "fields": [("Descripción:", "description")],
        "columns": [("description", "Descripción", 250)],
        "id_attr": "gender_id",
    },
    {
        "title": "Tipos de Seguro",
        "icon": "🛡️",
        "color": UIStyles.CARD_GREEN,
        "service_cls": InsuranceTypeService,
        "fields": [("Descripción:", "description")],
        "columns": [("description", "Descripción", 250)],
        "id_attr": "insurance_type_id",
    },
    {
        "title": "Estados de Póliza",
        "icon": "📋",
        "color": UIStyles.CARD_BLUE,
        "service_cls": PolicyStatusService,
        "fields": [("Descripción:", "description")],
        "columns": [("description", "Descripción", 250)],
        "id_attr": "policy_status_id",
    },
    {
        "title": "Tipos de Reaseguro",
        "icon": "🔄",
        "color": UIStyles.CARD_PURPLE,
        "service_cls": ReinsuranceTypeService,
        "fields": [("Descripción:", "description")],
        "columns": [("description", "Descripción", 250)],
        "id_attr": "reinsurance_type_id",
    },
]


class NomenclatorsPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=UIStyles.BG_LIGHT)
        self.parent_frame = parent
        self._current_view = None
        self._show_hub()

    def _clear(self):
        if self._current_view is not None:
            self._current_view.pack_forget()
            self._current_view.destroy()
            self._current_view = None

    def _show_hub(self):
        self._clear()
        container = tk.Frame(self, bg=UIStyles.BG_LIGHT)
        container.pack(fill="both", expand=True)
        self._current_view = container

        tk.Label(container, text="Catálogos del Sistema",
                 font=("Segoe UI", UIScale.font(22), "bold"),
                 fg=UIStyles.TEXT_PRIMARY, bg=UIStyles.BG_LIGHT
                 ).pack(pady=(UIScale.px(30), UIScale.px(10)))

        tk.Label(container, text="Seleccione un catálogo para gestionar sus datos maestros",
                 font=("Segoe UI", UIScale.font(11)),
                 fg=UIStyles.TEXT_SECONDARY, bg=UIStyles.BG_LIGHT
                 ).pack(pady=(0, UIScale.px(30)))

        cards_frame = tk.Frame(container, bg=UIStyles.BG_LIGHT)
        cards_frame.pack(expand=True, fill="both", padx=UIScale.px(40))
        cards_frame.grid_rowconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(0, weight=1)

        self._card_inner = tk.Frame(cards_frame, bg=UIStyles.BG_LIGHT)
        self._card_inner.grid(row=0, column=0, sticky="nsew")

        self._card_configs = NOMENCLATORS
        self._card_frames = []
        self._rebuild_cards()

        self._card_inner.bind("<Configure>", self._on_cards_resize)

    def _rebuild_cards(self):
        for child in self._card_inner.winfo_children():
            child.destroy()
        self._card_frames = []
        for cfg in self._card_configs:
            self._card_frames.append(self._create_card(self._card_inner, cfg))

    def _on_cards_resize(self, event):
        avail = event.width
        p = UIScale.px
        gap = p(20)
        min_card_w = p(180)
        max_card_w = p(260)
        cols = max(1, min(len(self._card_configs), (avail + gap) // (max_card_w + gap)))
        card_w = (avail - (cols - 1) * gap) // cols
        card_w = max(min_card_w, min(max_card_w, card_w))
        card_h = int(card_w * 0.75)

        for i, card in enumerate(self._card_frames):
            row = i // cols
            col = i % cols
            card.grid(row=row, column=col, padx=gap // 2, pady=gap // 2, sticky="nsew")
            card.configure(width=card_w, height=card_h)
            self._card_inner.grid_columnconfigure(col, weight=0)
        for i in range(cols):
            self._card_inner.grid_columnconfigure(i, weight=1)
        for r in range((len(self._card_frames) + cols - 1) // cols):
            self._card_inner.grid_rowconfigure(r, weight=1)

    def _create_card(self, parent, cfg):
        card = tk.Frame(parent, bg=cfg["color"],
                        highlightbackground=cfg["color"], highlightthickness=0)
        card.pack_propagate(False)

        inner = tk.Frame(card, bg=cfg["color"])
        inner.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(inner, text=cfg["icon"], font=("Segoe UI", UIScale.font(34)),
                 bg=cfg["color"], fg="white").pack()
        tk.Label(inner, text=cfg["title"], font=("Segoe UI", UIScale.font(12), "bold"),
                 bg=cfg["color"], fg="white").pack(pady=(UIScale.px(8), 0))

        def on_enter(e):
            card.configure(bg=UIStyles.PRIMARY_DARK)
            inner.configure(bg=UIStyles.PRIMARY_DARK)
            for child in inner.winfo_children():
                child.configure(bg=UIStyles.PRIMARY_DARK)

        def on_leave(e):
            card.configure(bg=cfg["color"])
            inner.configure(bg=cfg["color"])
            for child in inner.winfo_children():
                child.configure(bg=cfg["color"])

        card.bind("<Enter>", on_enter)
        card.bind("<Leave>", on_leave)
        card.bind("<Button-1>", lambda e, c=cfg: self._show_catalog(c))
        for child in inner.winfo_children():
            child.bind("<Button-1>", lambda e, c=cfg: self._show_catalog(c))

        return card

    def _show_catalog(self, cfg):
        self._clear()
        container = tk.Frame(self, bg=UIStyles.BG_LIGHT)
        container.pack(fill="both", expand=True)
        self._current_view = container

        top_bar = tk.Frame(container, bg=UIStyles.BG_LIGHT)
        top_bar.pack(fill="x", padx=UIScale.px(20), pady=UIScale.px(10))

        tk.Button(top_bar, text="← Volver a Catálogos del Sistema",
                  font=("Segoe UI", UIScale.font(10)),
                  bg=UIStyles.CARD_BG, fg=UIStyles.TEXT_PRIMARY,
                  relief="solid", bd=1,
                  command=self._show_hub).pack(side="left")

        service = cfg["service_cls"]()
        combo_fields = cfg.get("combo_fields")
        panel = SimpleCatalogPanel(
            container,
            title=cfg["title"],
            service=service,
            fields=cfg["fields"],
            columns=cfg["columns"],
            id_attr=cfg["id_attr"],
            combo_fields=combo_fields,
        )
        panel.pack(fill="both", expand=True)
