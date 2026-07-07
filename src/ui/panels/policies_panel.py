import tkinter as tk
from tkinter import ttk, messagebox
from src.ui.ui_styles import UIStyles
from src.services.policy_service import PolicyService
from src.services.client_service import ClientService
from src.services.insurance_type_service import InsuranceTypeService
from src.services.policy_status_service import PolicyStatusService
from src.services.exceptions import ServiceError
from src.ui.ui_scaling import UIScale


class PoliciesPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=UIStyles.BG_LIGHT)
        self.policy_service = PolicyService()
        self.client_service = ClientService()
        self.insurance_type_service = InsuranceTypeService()
        self.policy_status_service = PolicyStatusService()

        tk.Label(self, text="Gestión de Pólizas",
                 font=("Segoe UI", UIScale.font(18), "bold"),
                 fg=UIStyles.TEXT_PRIMARY, bg=UIStyles.BG_LIGHT
                 ).pack(pady=(UIScale.px(20), UIScale.px(10)))

        p = UIScale.px
        form_frame = tk.Frame(self, bg=UIStyles.CARD_BG,
                              highlightbackground=UIStyles.BORDER, highlightthickness=1)
        form_frame.pack(fill="x", padx=p(40), pady=p(10))
        form_frame.grid_columnconfigure(1, weight=1)

        self.entries = {}
        row = 0
        for label, key in [("Fecha Inicio (YYYY-MM-DD):", "start_date"),
                           ("Fecha Vencimiento (YYYY-MM-DD):", "end_date"),
                           ("Prima Mensual:", "monthly_premium"),
                           ("Monto Asegurado:", "insured_amount"),
                           ("Motivo de Cancelación:", "cancellation_reason")]:
            tk.Label(form_frame, text=label, font=("Segoe UI", UIScale.font(10)),
                     bg=UIStyles.CARD_BG).grid(row=row, column=0, sticky="w", padx=p(10), pady=p(3))
            entry = ttk.Entry(form_frame, font=("Segoe UI", UIScale.font(10)))
            entry.grid(row=row, column=1, padx=p(10), pady=p(3), sticky="ew")
            self.entries[key] = entry
            row += 1

        self._load_combos(form_frame, len(self.entries))
        self._build_buttons()
        self._build_table()
        self._refresh()

    def _load_combos(self, parent, start_row):
        p = UIScale.px

        combos = [
            ("Cliente:", "client_id", self.client_service, "first_name", "client_id"),
            ("Tipo de Seguro:", "insurance_type_id", self.insurance_type_service, "description", "insurance_type_id"),
            ("Estado:", "policy_status_id", self.policy_status_service, "description", "policy_status_id"),
        ]

        for i, (label, key, svc, attr, id_attr) in enumerate(combos, start=start_row):
            tk.Label(parent, text=label,
                     font=("Segoe UI", UIScale.font(10)),
                     bg=UIStyles.CARD_BG).grid(row=i, column=0, sticky="w", padx=p(10), pady=p(3))

            combo = ttk.Combobox(parent, state="readonly",
                                 font=("Segoe UI", UIScale.font(10)))
            combo.grid(row=i, column=1, padx=p(10), pady=p(3), sticky="ew")

            items = svc.get_all()

            combo["values"] = [getattr(it, attr) for it in items]

            self.entries[key] = combo
            self.entries[f"{key}_data"] = {
                getattr(it, attr): getattr(it, id_attr)
                for it in items
            }
            print("ENTRIES FINAL:", self.entries.keys())

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

        self.tree = ttk.Treeview(
            tree_frame,
            columns=(
                "num", "client", "type", "status",
                "start", "end", "premium", "amount", "reason",
                "client_id", "type_id", "status_id"
            ),
            show="headings"
        )

        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree_col_config = [
            ("num", "Póliza #", 70),
            ("client", "Cliente", 180),
            ("type", "Tipo Seguro", 120),
            ("status", "Estado", 100),
            ("start", "Inicio", 110),
            ("end", "Vencimiento", 110),
            ("premium", "Prima", 100),
            ("amount", "Monto", 120),
            ("reason", "Motivo Cancelación", 180),
        ]
        for col, text, width in self.tree_col_config:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=UIScale.px(width))
            self.tree.column("client_id", width=0, stretch=False)
            self.tree.column("type_id", width=0, stretch=False)
            self.tree.column("status_id", width=0, stretch=False)

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
                if map_key in self.entries:
                    mapping = self.entries.get(f"{k}_data", {})
                    if val in mapping:
                        data[k] = mapping[val]
            else:
                if val:
                    data[k] = val
        try:
            self.policy_service.create(**data)
        except ServiceError as e:
            messagebox.showerror("Error", str(e))
            return
        messagebox.showinfo("Éxito", "Póliza guardada")
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
        data = {}
        for k, v in self.entries.items():
            if k.endswith("_data"):
                continue

            val = v.get()
            if not val:
                continue

            if isinstance(v, ttk.Combobox):
                map_key = f"{k}_data"
                if map_key in self.entries:
                    mapping = self.entries[map_key]
                    if val in mapping:
                        data[k] = mapping[val]
            else:
                data[k] = val
        try:
            self.policy_service.update(item["values"][0], **data)
        except ServiceError as e:
            messagebox.showerror("Error", str(e))
            return
        messagebox.showinfo("Éxito", "Póliza actualizada")
        self._clear_form()
        self._refresh()

    def _delete(self):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        if messagebox.askyesno("Confirmar", "¿Eliminar póliza?"):
            try:
                self.policy_service.delete(item["values"][0])
            except ServiceError as e:
                messagebox.showerror("Error", str(e))
                return
            self._clear_form()
            self._refresh()

    def _on_select(self, event):
        selected = self.tree.focus()
        if not selected:
            return

        values = self.tree.item(selected)["values"]

        self.entries["start_date"].delete(0, "end")
        self.entries["start_date"].insert(0, values[4])

        self.entries["end_date"].delete(0, "end")
        self.entries["end_date"].insert(0, values[5])

        self.entries["monthly_premium"].delete(0, "end")
        self.entries["monthly_premium"].insert(0, values[6])

        self.entries["insured_amount"].delete(0, "end")
        self.entries["insured_amount"].insert(0, values[7])

        self.entries["cancellation_reason"].delete(0, "end")
        self.entries["cancellation_reason"].insert(0, values[8])

        # 🔥 COMBOS YA CON IDS CORRECTOS
        self.entries["client_id"].set(values[9])
        self.entries["insurance_type_id"].set(values[10])
        self.entries["policy_status_id"].set(values[11])

    def _refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for p in self.policy_service.get_all():
            self.tree.insert("", "end", values=(
                p.policy_number,

                # 👇 TEXTO PARA MOSTRAR
                str(p.client),
                str(p.insurance_type),
                str(p.policy_status),

                p.start_date,
                p.end_date,
                p.monthly_premium,
                p.insured_amount,
                p.cancellation_reason if p.cancellation_reason else "-",

                # 👇 IDS OCULTOS (IMPORTANTE)
                p.client_id,
                p.insurance_type_id,
                p.policy_status_id
            ))