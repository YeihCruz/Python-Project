import tkinter as tk
from tkinter import ttk, messagebox
from src.ui.ui_styles import UIStyles
from src.services.agency_service import AgencyService
from src.services.exceptions import ServiceError
from src.ui.ui_scaling import UIScale


class AgencyPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=UIStyles.BG_LIGHT)
        self.agency_service = AgencyService()

        tk.Label(self, text="Gestión de Agencia",
                 font=("Segoe UI", UIScale.font(18), "bold"),
                 fg=UIStyles.TEXT_PRIMARY, bg=UIStyles.BG_LIGHT
                 ).pack(pady=(UIScale.px(20), UIScale.px(10)))

        form_frame = tk.Frame(self, bg=UIStyles.CARD_BG,
                              highlightbackground=UIStyles.BORDER, highlightthickness=1)
        form_frame.pack(fill="x", padx=UIScale.px(40), pady=UIScale.px(10))
        form_frame.grid_columnconfigure(1, weight=1)

        self.entries = {}
        p = UIScale.px
        for i, (label, key) in enumerate([
            ("Nombre:", "name"), ("Dirección:", "address"), ("Teléfono:", "phone"),
            ("Correo Electrónico:", "email"), ("Director General:", "general_director"),
            ("Gerente de Seguros:", "insurance_manager"), ("Gerente de Reclamos:", "claims_manager"),
        ]):
            tk.Label(form_frame, text=label, font=("Segoe UI", UIScale.font(10)),
                     bg=UIStyles.CARD_BG).grid(row=i, column=0, sticky="w", padx=p(10), pady=p(3))
            entry = ttk.Entry(form_frame, font=("Segoe UI", UIScale.font(10)))
            entry.grid(row=i, column=1, padx=p(10), pady=p(3), sticky="ew")
            self.entries[key] = entry

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

        tree_frame = tk.Frame(self, bg=UIStyles.BG_LIGHT)
        tree_frame.pack(fill="both", expand=True, padx=p(40), pady=p(10))
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=(
                "id",
                "name",
                "address",
                "phone",
                "email",
                "general_director",
                "insurance_manager",
                "claims_manager"
            ),
            show="headings"
        )

        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree_col_config = [
            ("id", "ID", 50),
            ("name", "Nombre", 140),
            ("address", "Dirección", 160),
            ("phone", "Teléfono", 120),
            ("email", "Correo", 180),
            ("general_director", "Director General", 160),
            ("insurance_manager", "Gerente Seguros", 160),
            ("claims_manager", "Gerente Reclamos", 160),
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
        data = {k: v.get() for k, v in self.entries.items()}
        try:
            self.agency_service.create(**data)
        except ServiceError as e:
            messagebox.showerror("Error", str(e))
            return
        messagebox.showinfo("Éxito", "Agencia guardada")
        self._clear_form()
        self._refresh()

    def _clear_form(self):
        for e in self.entries.values():
            e.delete(0, "end")

    def _update(self):
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        agency_id = item["values"][0]

        data = {
            "name": self.entries["name"].get(),
            "address": self.entries["address"].get(),
            "phone": self.entries["phone"].get(),
            "email": self.entries["email"].get(),
            "general_director": self.entries["general_director"].get(),
            "insurance_manager": self.entries["insurance_manager"].get(),
            "claims_manager": self.entries["claims_manager"].get(),
        }

        try:
            self.agency_service.update(agency_id, **data)
        except ServiceError as e:
            messagebox.showerror("Error", str(e))
            return

        messagebox.showinfo("Éxito", "Agencia actualizada")
        self._clear_form()
        self._refresh()

    def _delete(self):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        if messagebox.askyesno("Confirmar", "¿Eliminar agencia?"):
            try:
                self.agency_service.delete(item["values"][0])
            except ServiceError as e:
                messagebox.showerror("Error", str(e))
                return
            self._clear_form()
            self._refresh()

    def _on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0])["values"]

        self.entries["name"].delete(0, "end")
        self.entries["name"].insert(0, values[1])

        self.entries["address"].delete(0, "end")
        self.entries["address"].insert(0, values[2])

        self.entries["phone"].delete(0, "end")
        self.entries["phone"].insert(0, values[3])

        self.entries["email"].delete(0, "end")
        self.entries["email"].insert(0, values[4])

        self.entries["general_director"].delete(0, "end")
        self.entries["general_director"].insert(0, values[5])

        self.entries["insurance_manager"].delete(0, "end")
        self.entries["insurance_manager"].insert(0, values[6])

        self.entries["claims_manager"].delete(0, "end")
        self.entries["claims_manager"].insert(0, values[7])

    def _refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for a in self.agency_service.get_all():
            self.tree.insert("", "end", values=(
                a.agency_id,
                a.name,
                a.address,
                a.phone,
                a.email,
                a.general_director,
                a.insurance_manager,
                a.claims_manager
            ))
