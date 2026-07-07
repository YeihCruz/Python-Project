import tkinter as tk
from tkinter import ttk, messagebox
from src.ui.ui_styles import UIStyles
from src.services.client_service import ClientService
from src.services.country_service import CountryService
from src.services.gender_service import GenderService
from src.services.agency_service import AgencyService
from src.services.exceptions import ServiceError
from src.ui.ui_scaling import UIScale


class ClientsPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=UIStyles.BG_LIGHT)
        self.client_service = ClientService()
        self.country_service = CountryService()
        self.gender_service = GenderService()
        self.agency_service = AgencyService()

        tk.Label(self, text="Gestión de Clientes",
                 font=("Segoe UI", UIScale.font(18), "bold"),
                 fg=UIStyles.TEXT_PRIMARY, bg=UIStyles.BG_LIGHT
                 ).pack(pady=(UIScale.px(20), UIScale.px(10)))

        form_frame = tk.Frame(self, bg=UIStyles.CARD_BG,
                              highlightbackground=UIStyles.BORDER, highlightthickness=1)
        form_frame.pack(fill="x", padx=UIScale.px(40), pady=UIScale.px(10))
        form_frame.grid_columnconfigure(1, weight=1)

        fields = [
            ("Nombre:", "first_name"), ("Apellido:", "last_name"),
            ("Identificación:", "identification_number"), ("Edad:", "age"),
            ("Dirección:", "address"), ("Teléfono:", "phone"), ("Correo Electrónico:", "email"),
        ]
        self.entries = {}
        p = UIScale.px
        for i, (label, key) in enumerate(fields):
            tk.Label(form_frame, text=label, font=("Segoe UI", UIScale.font(10)),
                     bg=UIStyles.CARD_BG).grid(row=i, column=0, sticky="w", padx=p(10), pady=p(3))
            entry = ttk.Entry(form_frame, font=("Segoe UI", UIScale.font(10)))
            entry.grid(row=i, column=1, padx=p(10), pady=p(3), sticky="ew")
            self.entries[key] = entry

        self._load_combos(form_frame)
        self._build_buttons()
        self._build_table()

    def _load_combos(self, parent):
        row = len(self.entries)
        p = UIScale.px
        for label, key, svc, attr in [
            ("Agencia:", "agency_id", self.agency_service, "name"),
            ("Género:", "gender_id", self.gender_service, "description"),
            ("País:", "country_id", self.country_service, "name"),
        ]:
            tk.Label(parent, text=label, font=("Segoe UI", UIScale.font(10)),
                     bg=UIStyles.CARD_BG).grid(row=row, column=0, sticky="w", padx=p(10), pady=p(3))
            combo = ttk.Combobox(parent, state="readonly", font=("Segoe UI", UIScale.font(10)))
            combo.grid(row=row, column=1, padx=p(10), pady=p(3), sticky="ew")
            items = svc.get_all()
            combo_map = {str(item): getattr(item, attr) for item in items}
            combo["values"] = list(combo_map.keys())
            self.entries[key] = combo
            self.entries[f"{key}_map"] = combo_map
            self.entries[f"{key}_data"] = {getattr(item, attr): item for item in items}
            row += 1

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

        self.tree = ttk.Treeview(tree_frame, columns=("id", "first_name", "last_name", "id_number", "email"),
                                 show="headings")
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree_col_config = [
            ("id", "ID", 50), ("first_name", "Nombre", 140), ("last_name", "Apellido", 140),
            ("id_number", "Cédula", 120), ("email", "Correo Electrónico", 180)
        ]
        for col, text, width in self.tree_col_config:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=UIScale.px(width))

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.bind("<Map>", self._on_tree_map)
        self.tree.bind("<ButtonRelease-1>", self._on_select)
        self._refresh()

    def _on_tree_map(self, event):
        UIScale.configure_tree_columns(self.tree, self.tree_col_config)

    def _save(self):
        data = {}
        for k, v in self.entries.items():
            if k.endswith("_map") or k.endswith("_data"):
                continue
            val = v.get()
            if isinstance(v, ttk.Combobox):
                if val:
                    map_key = f"{k}_data"
                    if map_key in self.entries:
                        obj = self.entries[map_key].get(val)
                        if obj:
                            data[k] = obj.key if hasattr(obj, 'key') else obj.id if hasattr(obj, 'id') else getattr(obj, k)
            else:
                if val:
                    data[k] = val
        try:
            self.client_service.create(**data)
        except ServiceError as e:
            messagebox.showerror("Error", str(e))
            return
        messagebox.showinfo("Éxito", "Cliente guardado")
        self._clear_form()
        self._refresh()

    def _clear_form(self):
        for key, e in self.entries.items():
            if key.endswith("_map") or key.endswith("_data"):
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
        client_id = item["values"][0]

        data = {}

        # campos normales
        for k, v in self.entries.items():
            if k.endswith("_map") or k.endswith("_data"):
                continue

            val = v.get()
            if not val:
                continue

            # 🔴 CONVERSIÓN CRÍTICA PARA COMBOBOXES
            if k in ("agency_id", "gender_id", "country_id"):
                # convertir texto visible → objeto real → ID
                obj_map = self.entries[f"{k}_data"]

                obj = obj_map.get(val)

                if obj:
                    # extraer ID correcto
                    if hasattr(obj, "agency_id"):
                        data[k] = obj.agency_id
                    elif hasattr(obj, "gender_id"):
                        data[k] = obj.gender_id
                    elif hasattr(obj, "country_id"):
                        data[k] = obj.country_id
            else:
                data[k] = val

        try:
            self.client_service.update(client_id, **data)
        except ServiceError as e:
            messagebox.showerror("Error", str(e))
            return

        messagebox.showinfo("Éxito", "Cliente actualizado")
        self._clear_form()
        self._refresh()

    def _delete(self):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        if messagebox.askyesno("Confirmar", "¿Eliminar cliente?"):
            try:
                self.client_service.delete(item["values"][0])
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
        client_id = item["values"][0]

        client = self.client_service.get_by_id(client_id)

        if not client:
            return

        # Nombre
        self.entries["first_name"].delete(0, "end")
        self.entries["first_name"].insert(0, client.first_name)

        # Apellido
        self.entries["last_name"].delete(0, "end")
        self.entries["last_name"].insert(0, client.last_name)

        # Cédula
        self.entries["identification_number"].delete(0, "end")
        self.entries["identification_number"].insert(
            0,
            client.identification_number
        )

        # Edad
        self.entries["age"].delete(0, "end")
        self.entries["age"].insert(0, str(client.age))

        # Dirección
        self.entries["address"].delete(0, "end")
        self.entries["address"].insert(0, client.address)

        # Teléfono
        self.entries["phone"].delete(0, "end")
        self.entries["phone"].insert(0, client.phone)

        # Correo
        self.entries["email"].delete(0, "end")
        self.entries["email"].insert(0, client.email)

        # Agencia
        agency_obj = next(
            (
                obj
                for obj in self.entries["agency_id_data"].values()
                if obj.agency_id == client.agency_id
            ),
            None
        )

        if agency_obj:
            self.entries["agency_id"].set(str(agency_obj))

        # Género
        gender_obj = next(
            (
                obj
                for obj in self.entries["gender_id_data"].values()
                if obj.gender_id == client.gender_id
            ),
            None
        )

        if gender_obj:
            self.entries["gender_id"].set(str(gender_obj))

        # País
        country_obj = next(
            (
                obj
                for obj in self.entries["country_id_data"].values()
                if obj.country_id == client.country_id
            ),
            None
        )

        if country_obj:
            self.entries["country_id"].set(str(country_obj))

    def _refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for c in self.client_service.get_all():
            self.tree.insert("", "end", values=(
                c.client_id, c.first_name, c.last_name,
                c.identification_number, c.email))
