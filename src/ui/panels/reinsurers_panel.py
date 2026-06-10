import tkinter as tk
from tkinter import ttk, messagebox
from src.ui.ui_styles import UIStyles
from src.services.reinsurer_service import ReinsurerService
from src.services.agency_service import AgencyService
from src.services.reinsurance_type_service import ReinsuranceTypeService
from src.services.country_service import CountryService


class ReinsurersPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=UIStyles.BG_LIGHT)
        self.reinsurer_service = ReinsurerService()
        self.agency_service = AgencyService()
        self.reinsurance_type_service = ReinsuranceTypeService()
        self.country_service = CountryService()

        tk.Label(self, text="Gestión de Reaseguradoras",
                 font=("Segoe UI", 18, "bold"),
                 fg=UIStyles.TEXT_PRIMARY, bg=UIStyles.BG_LIGHT).pack(pady=20)

        form_frame = tk.Frame(self, bg=UIStyles.CARD_BG, highlightbackground=UIStyles.BORDER, highlightthickness=1)
        form_frame.pack(fill="x", padx=40, pady=10)

        self.entries = {}
        tk.Label(form_frame, text="Name:", font=("Segoe UI", 10),
                 bg=UIStyles.CARD_BG).grid(row=0, column=0, sticky="w", padx=10, pady=3)
        self.entries["name"] = ttk.Entry(form_frame, font=("Segoe UI", 10))
        self.entries["name"].grid(row=0, column=1, padx=10, pady=3, sticky="ew")

        self._load_combos(form_frame, 1)
        self._build_buttons()
        self._build_table()
        self._refresh()

    def _load_combos(self, parent, start_row):
        for label, key, svc, id_attr in [
            ("Agency:", "agency_id", self.agency_service, "agency_id"),
            ("Reinsurance Type:", "reinsurance_type_id", self.reinsurance_type_service, "reinsurance_type_id"),
            ("Country:", "country_id", self.country_service, "country_id"),
        ]:
            tk.Label(parent, text=label, font=("Segoe UI", 10),
                     bg=UIStyles.CARD_BG).grid(row=start_row, column=0, sticky="w", padx=10, pady=3)
            combo = ttk.Combobox(parent, state="readonly", font=("Segoe UI", 10))
            combo.grid(row=start_row, column=1, padx=10, pady=3, sticky="ew")
            items = svc.get_all()
            combo["values"] = [str(it) for it in items]
            self.entries[key] = combo
            self.entries[f"{key}_data"] = {str(it): getattr(it, id_attr) for it in items}
            start_row += 1

    def _build_buttons(self):
        btn_frame = tk.Frame(self, bg=UIStyles.BG_LIGHT)
        btn_frame.pack(pady=10)
        for text, cmd in [("Guardar", self._save), ("Actualizar", self._update), ("Eliminar", self._delete)]:
            tk.Button(btn_frame, text=text, font=("Segoe UI", 10, "bold"),
                      relief="flat", padx=20, command=cmd).pack(side="left", padx=5)

    def _build_table(self):
        self.tree = ttk.Treeview(self, columns=("id", "name", "agency", "type", "country"),
                                 show="headings", height=15)
        for col, width in [("id", 50), ("name", 150), ("agency", 100),
                           ("type", 100), ("country", 100)]:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=width)
        self.tree.pack(fill="both", expand=True, padx=40, pady=10)

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
        self.reinsurer_service.create(**data)
        messagebox.showinfo("Éxito", "Reaseguradora guardada")
        self._refresh()

    def _update(self):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        data = {}
        for k, v in self.entries.items():
            if not k.endswith("_data"):
                val = v.get()
                if val:
                    data[k] = val
        self.reinsurer_service.update(item["values"][0], **data)
        messagebox.showinfo("Éxito", "Reaseguradora actualizada")
        self._refresh()

    def _delete(self):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        if messagebox.askyesno("Confirmar", "¿Eliminar reaseguradora?"):
            self.reinsurer_service.delete(item["values"][0])
            self._refresh()

    def _refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for r in self.reinsurer_service.get_all():
            self.tree.insert("", "end", values=(
                r.reinsurer_id, r.name, str(r.agency), str(r.reinsurance_type), str(r.country)))
