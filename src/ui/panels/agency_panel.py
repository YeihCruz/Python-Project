import tkinter as tk
from tkinter import ttk, messagebox
from src.ui.ui_styles import UIStyles
from src.services.agency_service import AgencyService


class AgencyPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=UIStyles.BG_LIGHT)
        self.agency_service = AgencyService()

        tk.Label(self, text="Gestión de Agencia",
                 font=("Segoe UI", 18, "bold"),
                 fg=UIStyles.TEXT_PRIMARY, bg=UIStyles.BG_LIGHT).pack(pady=20)

        form_frame = tk.Frame(self, bg=UIStyles.CARD_BG, highlightbackground=UIStyles.BORDER, highlightthickness=1)
        form_frame.pack(fill="x", padx=40, pady=10)

        self.entries = {}
        for i, (label, key) in enumerate([
            ("Name:", "name"), ("Address:", "address"), ("Phone:", "phone"),
            ("Email:", "email"), ("General Director:", "general_director"),
            ("Insurance Manager:", "insurance_manager"), ("Claims Manager:", "claims_manager"),
        ]):
            tk.Label(form_frame, text=label, font=("Segoe UI", 10),
                     bg=UIStyles.CARD_BG).grid(row=i, column=0, sticky="w", padx=10, pady=3)
            entry = ttk.Entry(form_frame, font=("Segoe UI", 10))
            entry.grid(row=i, column=1, padx=10, pady=3, sticky="ew")
            self.entries[key] = entry

        btn_frame = tk.Frame(self, bg=UIStyles.BG_LIGHT)
        btn_frame.pack(pady=10)
        for text, cmd in [("Guardar", self._save), ("Actualizar", self._update),
                          ("Eliminar", self._delete)]:
            tk.Button(btn_frame, text=text, font=("Segoe UI", 10, "bold"),
                      relief="flat", padx=20, command=cmd).pack(side="left", padx=5)

        self.tree = ttk.Treeview(self, columns=("id", "name", "email", "phone"),
                                 show="headings", height=15)
        for col, width in [("id", 50), ("name", 150), ("email", 150), ("phone", 100)]:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=width)
        self.tree.pack(fill="both", expand=True, padx=40, pady=10)
        self._refresh()

    def _save(self):
        data = {k: v.get() for k, v in self.entries.items()}
        self.agency_service.create(**data)
        messagebox.showinfo("Éxito", "Agencia guardada")
        self._refresh()

    def _update(self):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        data = {k: v.get() for k, v in self.entries.items() if v.get()}
        self.agency_service.update(item["values"][0], **data)
        messagebox.showinfo("Éxito", "Agencia actualizada")
        self._refresh()

    def _delete(self):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        if messagebox.askyesno("Confirmar", "¿Eliminar agencia?"):
            self.agency_service.delete(item["values"][0])
            self._refresh()

    def _refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for a in self.agency_service.get_all():
            self.tree.insert("", "end", values=(a.agency_id, a.name, a.email, a.phone))
