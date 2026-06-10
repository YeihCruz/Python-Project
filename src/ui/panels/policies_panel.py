import tkinter as tk
from tkinter import ttk, messagebox
from src.ui.ui_styles import UIStyles
from src.services.policy_service import PolicyService
from src.services.client_service import ClientService
from src.services.insurance_type_service import InsuranceTypeService
from src.services.policy_status_service import PolicyStatusService


class PoliciesPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=UIStyles.BG_LIGHT)
        self.policy_service = PolicyService()
        self.client_service = ClientService()
        self.insurance_type_service = InsuranceTypeService()
        self.policy_status_service = PolicyStatusService()

        tk.Label(self, text="Gestión de Pólizas",
                 font=("Segoe UI", 18, "bold"),
                 fg=UIStyles.TEXT_PRIMARY, bg=UIStyles.BG_LIGHT).pack(pady=20)

        form_frame = tk.Frame(self, bg=UIStyles.CARD_BG, highlightbackground=UIStyles.BORDER, highlightthickness=1)
        form_frame.pack(fill="x", padx=40, pady=10)

        self.entries = {}
        row = 0

        for label, key in [("Start Date (YYYY-MM-DD):", "start_date"),
                           ("End Date (YYYY-MM-DD):", "end_date"),
                           ("Monthly Premium:", "monthly_premium"),
                           ("Insured Amount:", "insured_amount"),
                           ("Cancellation Reason:", "cancellation_reason")]:
            tk.Label(form_frame, text=label, font=("Segoe UI", 10),
                     bg=UIStyles.CARD_BG).grid(row=row, column=0, sticky="w", padx=10, pady=3)
            entry = ttk.Entry(form_frame, font=("Segoe UI", 10))
            entry.grid(row=row, column=1, padx=10, pady=3, sticky="ew")
            self.entries[key] = entry
            row += 1

        self._load_combos(form_frame, row)
        self._build_buttons()
        self._build_table()
        self._refresh()

    def _load_combos(self, parent, start_row):
        for label, key, svc, attr, id_attr in [
            ("Client:", "client_id", self.client_service, "first_name", "client_id"),
            ("Insurance Type:", "insurance_type_id", self.insurance_type_service, "description", "insurance_type_id"),
            ("Status:", "policy_status_id", self.policy_status_service, "description", "policy_status_id"),
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
        self.tree = ttk.Treeview(self, columns=("num", "client", "type", "status", "start", "end"),
                                 show="headings", height=15)
        for col, width in [("num", 60), ("client", 150), ("type", 100),
                           ("status", 80), ("start", 100), ("end", 100)]:
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
                data_key = k
                map_key = f"{k}_data"
                if map_key in self.entries and val in self.entries[map_key]:
                    data[data_key] = self.entries[map_key][val]
            else:
                if val:
                    data[k] = val
        self.policy_service.create(**data)
        messagebox.showinfo("Éxito", "Póliza guardada")
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
        self.policy_service.update(item["values"][0], **data)
        messagebox.showinfo("Éxito", "Póliza actualizada")
        self._refresh()

    def _delete(self):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        if messagebox.askyesno("Confirmar", "¿Eliminar póliza?"):
            self.policy_service.delete(item["values"][0])
            self._refresh()

    def _refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for p in self.policy_service.get_all():
            self.tree.insert("", "end", values=(
                p.policy_number, str(p.client), str(p.insurance_type),
                str(p.policy_status), p.start_date, p.end_date))
