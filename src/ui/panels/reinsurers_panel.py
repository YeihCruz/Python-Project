import tkinter as tk
from tkinter import ttk, messagebox
from src.ui.ui_styles import UIStyles
from src.services.reinsurer_service import ReinsurerService
from src.services.agency_service import AgencyService
from src.services.reinsurance_type_service import ReinsuranceTypeService
from src.services.country_service import CountryService
from src.services.exceptions import ServiceError
from src.ui.ui_scaling import UIScale


class ReinsurersPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=UIStyles.BG_LIGHT)
        self.reinsurer_service = ReinsurerService()
        self.agency_service = AgencyService()
        self.reinsurance_type_service = ReinsuranceTypeService()
        self.country_service = CountryService()

        tk.Label(self, text="Gestión de Reaseguradoras",
                 font=("Segoe UI", UIScale.font(18), "bold"),
                 fg=UIStyles.TEXT_PRIMARY, bg=UIStyles.BG_LIGHT
                 ).pack(pady=(UIScale.px(20), UIScale.px(10)))

        p = UIScale.px
        form_frame = tk.Frame(self, bg=UIStyles.CARD_BG,
                              highlightbackground=UIStyles.BORDER, highlightthickness=1)
        form_frame.pack(fill="x", padx=p(40), pady=p(10))
        form_frame.grid_columnconfigure(1, weight=1)

        self.entries = {}
        tk.Label(form_frame, text="Nombre:", font=("Segoe UI", UIScale.font(10)),
                 bg=UIStyles.CARD_BG).grid(row=0, column=0, sticky="w", padx=p(10), pady=p(3))
        self.entries["name"] = ttk.Entry(form_frame, font=("Segoe UI", UIScale.font(10)))
        self.entries["name"].grid(row=0, column=1, padx=p(10), pady=p(3), sticky="ew")

        self._load_combos(form_frame, 1)
        self._build_buttons()
        self._build_table()
        self._refresh()

    def _load_combos(self, parent, start_row):
        p = UIScale.px
        for label, key, svc, id_attr in [
            ("Agencia:", "agency_id", self.agency_service, "agency_id"),
            ("Tipo de Reaseguro:", "reinsurance_type_id", self.reinsurance_type_service, "reinsurance_type_id"),
            ("País:", "country_id", self.country_service, "country_id"),
        ]:
            tk.Label(parent, text=label, font=("Segoe UI", UIScale.font(10)),
                     bg=UIStyles.CARD_BG).grid(row=start_row, column=0, sticky="w", padx=p(10), pady=p(3))
            combo = ttk.Combobox(parent, state="readonly", font=("Segoe UI", UIScale.font(10)))
            combo.grid(row=start_row, column=1, padx=p(10), pady=p(3), sticky="ew")
            items = svc.get_all()
            combo["values"] = [str(it) for it in items]
            self.entries[key] = combo
            self.entries[f"{key}_data"] = {str(it): getattr(it, id_attr) for it in items}
            start_row += 1

    def _build_buttons(self):
        p = UIScale.px
        btn_frame = tk.Frame(self, bg=UIStyles.BG_LIGHT)
        btn_frame.pack(pady=p(10))
        btn_colors = {
            "Guardar": (UIStyles.PRIMARY, "white"),
            "Actualizar": (UIStyles.CARD_ORANGE, "white"),
            "Eliminar": (UIStyles.CARD_RED, "white"),
        }
        for text, cmd in [("Guardar", self._save), ("Actualizar", self._update),
                          ("Eliminar", self._delete)]:
            bg, fg = btn_colors.get(text, (UIStyles.CARD_BG, UIStyles.TEXT_PRIMARY))
            tk.Button(btn_frame, text=text, bg=bg, fg=fg,
                      font=("Segoe UI", UIScale.font(10), "bold"),
                      relief="flat", padx=p(20), command=cmd).pack(side="left", padx=p(5))

    def _build_table(self):
        p = UIScale.px
        tree_frame = tk.Frame(self, bg=UIStyles.BG_LIGHT)
        tree_frame.pack(fill="both", expand=True, padx=p(40), pady=p(10))
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(tree_frame, columns=("id", "name", "agency", "type", "country"),
                                 show="headings")
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree_col_config = [
            ("id", "ID", 50), ("name", "Nombre", 180), ("agency", "Agencia", 130),
            ("type", "Tipo Reaseguro", 130), ("country", "País", 120)
        ]
        for col, text, width in self.tree_col_config:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=UIScale.px(width))

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.bind("<Map>", self._on_tree_map)
        self.tree.bind("<ButtonRelease-1>", self._on_select)

    def _on_tree_map(self, event):
        UIScale.configure_tree_columns(self.tree, self.tree_col_config)

    def _save(self):
        data = {}
        for k, v in self.entries.items():
            if k.endswith("_data"):
                continue
            val = v.get()
            if isinstance(v, ttk.Combobox):
                map_key = f"{k}_data"
                if map_key in self.entries and val in self.entries[map_key]:
                    data[k] = self.entries[map_key][val]
            else:
                if val:
                    data[k] = val
        try:
            self.reinsurer_service.create(**data)
        except ServiceError as e:
            messagebox.showerror("Error", str(e))
            return
        messagebox.showinfo("Éxito", "Reaseguradora guardada")
        self._clear_form()
        self._refresh()

    def _clear_form(self):
        for key, e in self.entries.items():
            if key.endswith("_data"):
                continue
            if isinstance(e, ttk.Combobox):
                e.set("")
            else:
                e.delete(0, "end")

    def _update(self):
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        reinsurer_id = item["values"][0]

        name = self.entries["name"].get()

        try:
            self.reinsurer_service.update(
                reinsurer_id,
                name=name
            )
        except ServiceError as e:
            messagebox.showerror("Error", str(e))
            return

        messagebox.showinfo("Éxito", "Reaseguradora actualizada")
        self._clear_form()
        self._refresh()

    def _delete(self):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        if messagebox.askyesno("Confirmar", "¿Eliminar reaseguradora?"):
            try:
                self.reinsurer_service.delete(item["values"][0])
            except ServiceError as e:
                messagebox.showerror("Error", str(e))
                return
            self._clear_form()
            self._refresh()

    def _on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        values = item["values"]

        # ENTRY simple
        self.entries["name"].delete(0, "end")
        self.entries["name"].insert(0, values[1])

        # COMBOS
        self.entries["agency_id"].set(values[2])
        self.entries["reinsurance_type_id"].set(values[3])
        self.entries["country_id"].set(values[4])

    def _refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for r in self.reinsurer_service.get_all():
            self.tree.insert("", "end", values=(
                r.reinsurer_id, r.name, str(r.agency), str(r.reinsurance_type), str(r.country)))
