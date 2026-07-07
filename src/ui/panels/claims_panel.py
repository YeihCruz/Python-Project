import tkinter as tk
from tkinter import ttk, messagebox
from src.ui.ui_styles import UIStyles
from src.services.claim_service import ClaimService
from src.services.claim_type_service import ClaimTypeService
from src.services.claim_status_service import ClaimStatusService
from src.services.policy_service import PolicyService
from src.services.exceptions import ServiceError
from src.ui.ui_scaling import UIScale


class ClaimsPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=UIStyles.BG_LIGHT)
        self.claim_service = ClaimService()
        self.claim_type_service = ClaimTypeService()
        self.claim_status_service = ClaimStatusService()
        self.policy_service = PolicyService()

        tk.Label(self, text="Gestión de Reclamos",
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
        for label, key in [("Fecha del Incidente (YYYY-MM-DD):", "incident_date"),
                           ("Monto Reclamado:", "claimed_amount"),
                           ("Monto Compensado:", "compensated_amount"),
                           ("Motivo de Rechazo:", "rejection_reason")]:
            tk.Label(form_frame, text=label, font=("Segoe UI", UIScale.font(10)),
                     bg=UIStyles.CARD_BG).grid(row=row, column=0, sticky="w", padx=p(10), pady=p(3))
            entry = ttk.Entry(form_frame, font=("Segoe UI", UIScale.font(10)))
            entry.grid(row=row, column=1, padx=p(10), pady=p(3), sticky="ew")
            self.entries[key] = entry
            row += 1

        self._load_combos(form_frame, row)
        self._build_buttons()
        self._build_table()
        self._refresh()

    def _load_combos(self, parent, start_row):
        p = UIScale.px

        combos = [
            ("Póliza:", "policy_number", self.policy_service, "policy_number"),
            ("Tipo de Reclamo:", "claim_type_id", self.claim_type_service, "description"),
            ("Estado del Reclamo:", "claim_status_id", self.claim_status_service, "description"),
        ]

        for label, key, svc, display_attr in combos:
            tk.Label(parent, text=label, bg=UIStyles.CARD_BG).grid(
                row=start_row, column=0, sticky="w", padx=p(10), pady=p(3)
            )

            combo = ttk.Combobox(parent, state="readonly")
            combo.grid(row=start_row, column=1, sticky="ew")

            items = svc.get_all()

            # texto visible
            combo["values"] = [getattr(it, display_attr) for it in items]

            # MAPA: texto -> OBJETO COMPLETO
            self.entries[key] = combo
            self.entries[f"{key}_map"] = {
                getattr(it, display_attr): it for it in items
            }

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
        tree_frame.pack(fill="both", expand=True, padx=p(20), pady=p(10))
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=(
                "num",
                "policy",
                "type",
                "status",
                "date",
                "claimed",
                "compensated",
                "reason"
            ),
            show="headings"
        )

        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.configure(height=18)

        columns = [
            ("num", "Reclamo #", 90),
            ("policy", "Póliza", 140),
            ("type", "Tipo", 160),
            ("status", "Estado", 140),
            ("date", "Fecha", 140),
            ("claimed", "Reclamado", 140),
            ("compensated", "Compensado", 140),
            ("reason", "Motivo", 220),
        ]

        for col, text, width in columns:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=0, column=1, sticky="ns")

        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.bind("<ButtonRelease-1>", self._on_select)
    def _on_tree_map(self, event):
        UIScale.configure_tree_columns(self.tree, self.tree_col_config)

    def _save(self):
        data = {}

        for k, v in self.entries.items():
            if k.endswith("_map"):
                continue

            val = v.get()

            if isinstance(v, ttk.Combobox):
                obj = self.entries[f"{k}_map"].get(val)

                if obj:
                    if k == "policy_number":
                        data[k] = obj.policy_number
                    elif k == "claim_type_id":
                        data[k] = obj.claim_type_id
                    elif k == "claim_status_id":
                        data[k] = obj.claim_status_id
            else:
                if val:
                    data[k] = val

        try:
            self.claim_service.create(**data)
        except ServiceError as e:
            messagebox.showerror("Error", str(e))
            return

        messagebox.showinfo("Éxito", "Reclamo guardado")
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

        claim_id = self.tree.item(selected[0])["values"][0]

        data = {}

        for k, v in self.entries.items():
            if k.endswith("_map"):
                continue

            val = v.get()

            if isinstance(v, ttk.Combobox):
                obj = self.entries[f"{k}_map"].get(val)

                if obj:
                    if k == "policy_number":
                        data[k] = obj.policy_number
                    elif k == "claim_type_id":
                        data[k] = obj.claim_type_id
                    elif k == "claim_status_id":
                        data[k] = obj.claim_status_id
            else:
                if val:
                    data[k] = val

        try:
            self.claim_service.update(claim_id, **data)
        except ServiceError as e:
            messagebox.showerror("Error", str(e))
            return

        messagebox.showinfo("Éxito", "Reclamo actualizado")
        self._clear_form()
        self._refresh()

    def _delete(self):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        if messagebox.askyesno("Confirmar", "¿Eliminar reclamo?"):
            try:
                self.claim_service.delete(item["values"][0])
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

        self.entries["incident_date"].delete(0, "end")
        self.entries["incident_date"].insert(0, values[4])

        self.entries["claimed_amount"].delete(0, "end")
        self.entries["claimed_amount"].insert(0, values[5])

        self.entries["compensated_amount"].delete(0, "end")
        self.entries["compensated_amount"].insert(0, values[6])

        self.entries["rejection_reason"].delete(0, "end")
        self.entries["rejection_reason"].insert(0, values[7])

        # COMBOS (TEXTOS, NO IDS)
        self.entries["policy_number"].set(values[1])
        self.entries["claim_type_id"].set(values[2])
        self.entries["claim_status_id"].set(values[3])

    def _refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for (
                claim_number,
                policy_id,
                type_id,
                status_id,
                date,
                claimed,
                compensated,
                reason,
                policy,
                claim_type,
                claim_status
        ) in self.claim_service.get_all():
            self.tree.insert("", "end", values=(
                claim_number,
                policy.policy_number,
                claim_type.description,
                claim_status.description,
                date,
                claimed,
                compensated or 0,
                reason or "-"
            ))