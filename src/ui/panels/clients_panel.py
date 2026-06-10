import tkinter as tk
from tkinter import ttk, messagebox
from src.ui.ui_styles import UIStyles
from src.services.client_service import ClientService
from src.services.country_service import CountryService
from src.services.gender_service import GenderService
from src.services.agency_service import AgencyService


class ClientsPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=UIStyles.BG_LIGHT)
        self.client_service = ClientService()
        self.country_service = CountryService()
        self.gender_service = GenderService()
        self.agency_service = AgencyService()

        tk.Label(self, text="Gestión de Clientes",
                 font=("Segoe UI", 18, "bold"),
                 fg=UIStyles.TEXT_PRIMARY, bg=UIStyles.BG_LIGHT).pack(pady=20)

        form_frame = tk.Frame(self, bg=UIStyles.CARD_BG, highlightbackground=UIStyles.BORDER, highlightthickness=1)
        form_frame.pack(fill="x", padx=40, pady=10)

        fields = [
            ("First Name:", "first_name"), ("Last Name:", "last_name"),
            ("ID Number:", "identification_number"), ("Age:", "age"),
            ("Address:", "address"), ("Phone:", "phone"), ("Email:", "email"),
        ]
        self.entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(form_frame, text=label, font=("Segoe UI", 10),
                     bg=UIStyles.CARD_BG).grid(row=i, column=0, sticky="w", padx=10, pady=3)
            entry = ttk.Entry(form_frame, font=("Segoe UI", 10))
            entry.grid(row=i, column=1, padx=10, pady=3, sticky="ew")
            self.entries[key] = entry

        self._load_combos(form_frame)
        self._build_buttons()
        self._build_table()

    def _load_combos(self, parent):
        row = len(self.entries)

        for label, key, svc, attr in [
            ("Agency:", "agency_id", self.agency_service, "name"),
            ("Gender:", "gender_id", self.gender_service, "description"),
            ("Country:", "country_id", self.country_service, "name"),
        ]:
            tk.Label(parent, text=label, font=("Segoe UI", 10),
                     bg=UIStyles.CARD_BG).grid(row=row, column=0, sticky="w", padx=10, pady=3)
            combo = ttk.Combobox(parent, state="readonly", font=("Segoe UI", 10))
            combo.grid(row=row, column=1, padx=10, pady=3, sticky="ew")
            items = svc.get_all()
            combo_map = {str(item): getattr(item, attr) for item in items}
            combo["values"] = list(combo_map.keys())
            self.entries[key] = combo
            self.entries[f"{key}_map"] = {str(item): getattr(item, attr) for item in items}
            self.entries[f"{key}_data"] = {getattr(item, attr): item for item in items}
            row += 1

    def _build_buttons(self):
        btn_frame = tk.Frame(self, bg=UIStyles.BG_LIGHT)
        btn_frame.pack(pady=10)
        for text, cmd in [("Guardar", self._save), ("Actualizar", self._update),
                          ("Eliminar", self._delete)]:
            tk.Button(btn_frame, text=text, font=("Segoe UI", 10, "bold"),
                      relief="flat", padx=20,
                      command=cmd).pack(side="left", padx=5)

    def _build_table(self):
        self.tree = ttk.Treeview(self, columns=("id", "first_name", "last_name", "id_number", "email"),
                                 show="headings", height=15)
        for col, width in [("id", 50), ("first_name", 120), ("last_name", 120),
                           ("id_number", 100), ("email", 150)]:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=width)
        self.tree.pack(fill="both", expand=True, padx=40, pady=10)
        self.tree.bind("<ButtonRelease-1>", self._on_select)
        self._refresh()

    def _save(self):
        data = {}
        for k, v in self.entries.items():
            if k.endswith("_map") or k.endswith("_data"):
                continue
            val = v.get()
            if isinstance(v, ttk.Combobox):
                key = k
                if val:
                    map_key = f"{k}_data"
                    if map_key in self.entries:
                        obj = self.entries[map_key].get(val)
                        if obj:
                            data[key] = obj.key if hasattr(obj, 'key') else obj.id if hasattr(obj, 'id') else getattr(obj, k)
            else:
                if val:
                    data[k] = val
        self.client_service.create(**data)
        messagebox.showinfo("Éxito", "Cliente guardado")
        self._refresh()

    def _update(self):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        client_id = item["values"][0]
        data = {}
        for k, v in self.entries.items():
            if not k.endswith("_map") and not k.endswith("_data"):
                val = v.get()
                if val:
                    data[k] = val
        self.client_service.update(client_id, **data)
        messagebox.showinfo("Éxito", "Cliente actualizado")
        self._refresh()

    def _delete(self):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        if messagebox.askyesno("Confirmar", "¿Eliminar cliente?"):
            self.client_service.delete(item["values"][0])
            self._refresh()

    def _on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        vals = item["values"]

    def _refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for c in self.client_service.get_all():
            self.tree.insert("", "end", values=(
                c.client_id, c.first_name, c.last_name,
                c.identification_number, c.email))
