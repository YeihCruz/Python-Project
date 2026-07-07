import tkinter as tk
from tkinter import ttk, messagebox
from src.ui.ui_styles import UIStyles
from src.services.exceptions import ServiceError
from src.ui.ui_scaling import UIScale


class SimpleCatalogPanel(tk.Frame):
    def __init__(self, parent, title, service, fields, columns, id_attr="id", combo_fields=None):
        super().__init__(parent, bg=UIStyles.BG_LIGHT)
        self.service = service
        self.fields = fields
        self.columns = columns
        self.id_attr = id_attr
        self.combo_fields = combo_fields or {}

        tk.Label(self, text=title,
                 font=("Segoe UI", UIScale.font(18), "bold"),
                 fg=UIStyles.TEXT_PRIMARY, bg=UIStyles.BG_LIGHT
                 ).pack(pady=(UIScale.px(20), UIScale.px(10)))

        p = UIScale.px
        form_frame = tk.Frame(self, bg=UIStyles.CARD_BG,
                              highlightbackground=UIStyles.BORDER, highlightthickness=1)
        form_frame.pack(fill="x", padx=p(40), pady=p(10))
        form_frame.grid_columnconfigure(1, weight=1)

        self.entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(form_frame, text=label, font=("Segoe UI", UIScale.font(10)),
                     bg=UIStyles.CARD_BG).grid(row=i, column=0, sticky="w", padx=p(10), pady=p(4))
            values = self.combo_fields.get(key)
            if values:
                entry = ttk.Combobox(form_frame, values=values,
                                     font=("Segoe UI", UIScale.font(10)), state="readonly")
            else:
                entry = ttk.Entry(form_frame, font=("Segoe UI", UIScale.font(10)))
            entry.grid(row=i, column=1, padx=p(10), pady=p(4), sticky="ew")
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

        id_col = ("id", "ID", 50)
        col_defs = [id_col] + columns
        col_keys = [c[0] for c in col_defs]
        style = ttk.Style()
        style.configure("Catalog.Treeview.Heading",
                        background=UIStyles.PRIMARY,
                        foreground="white",
                        font=("Segoe UI", UIScale.font(10), "bold"),
                        borderwidth=0)
        style.map("Catalog.Treeview.Heading",
                  background=[("active", UIStyles.PRIMARY_DARK)])
        self.tree = ttk.Treeview(tree_frame, columns=col_keys, show="headings",
                                 style="Catalog.Treeview")
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree_col_defs = col_defs
        for col_key, col_text, col_width in col_defs:
            self.tree.heading(col_key, text=col_text)
            self.tree.column(col_key, width=UIScale.px(col_width))

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.bind("<Map>", self._on_tree_map)
        self.tree.bind("<ButtonRelease-1>", self._on_select)
        self._refresh()

    def _on_tree_map(self, event):
        self.tree.update_idletasks()
        avail = self.tree.winfo_width() - 20
        if avail > 50:
            total = sum(w for _, _, w in self.tree_col_defs)
            ratios = [w / total for _, _, w in self.tree_col_defs]
            for (ck, _, _), ratio in zip(self.tree_col_defs, ratios):
                new_w = max(UIScale.px(50), int(avail * ratio))
                self.tree.column(ck, width=new_w)

    def _get_record_id(self, item_values):
        return int(item_values[0])

    def _save(self):
        data = {k: v.get() for k, v in self.entries.items()}
        if not all(data.values()):
            messagebox.showwarning("Campos incompletos", "Todos los campos son obligatorios")
            return
        try:
            self.service.create(**data)
        except ServiceError as e:
            messagebox.showerror("Error", str(e))
            return
        messagebox.showinfo("Éxito", "Registro guardado correctamente")
        self._clear_form()
        self._refresh()

    def _update(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Seleccionar", "Seleccione un registro")
            return
        item = self.tree.item(selected[0])
        data = {k: v.get() for k, v in self.entries.items() if v.get()}
        if not data:
            messagebox.showwarning("Datos", "Complete al menos un campo")
            return
        try:
            self.service.update(self._get_record_id(item["values"]), **data)
        except ServiceError as e:
            messagebox.showerror("Error", str(e))
            return
        messagebox.showinfo("Éxito", "Registro actualizado correctamente")
        self._clear_form()
        self._refresh()

    def _delete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Seleccionar", "Seleccione un registro")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar registro?"):
            item = self.tree.item(selected[0])
            try:
                self.service.delete(self._get_record_id(item["values"]))
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
        vals = item["values"]
        for i, (_, key) in enumerate(self.fields):
            entry = self.entries[key]
            if isinstance(entry, ttk.Combobox):
                entry.set(str(vals[i + 1] or ""))
            else:
                entry.delete(0, "end")
                entry.insert(0, str(vals[i + 1] or ""))

    def _clear_form(self):
        for key, e in self.entries.items():
            if isinstance(e, ttk.Combobox):
                e.set("")
            else:
                e.delete(0, "end")

    def _refresh(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        records = self.service.get_all()
        for r in records:
            row_id = getattr(r, self.id_attr)
            row_vals = [getattr(r, c[0], "") for c in self.columns]
            self.tree.insert("", "end", values=(row_id, *row_vals))
