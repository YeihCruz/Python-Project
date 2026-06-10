import tkinter as tk
from tkinter import ttk, messagebox
from src.ui.ui_styles import UIStyles
from src.services.user_service import UserService
from src.services.role_service import RoleService


class UsersPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=UIStyles.BG_LIGHT)
        self.user_service = UserService()
        self.role_service = RoleService()

        tk.Label(self, text="Gestión de Usuarios",
                 font=("Segoe UI", 18, "bold"),
                 fg=UIStyles.TEXT_PRIMARY, bg=UIStyles.BG_LIGHT).pack(pady=20)

        form_frame = tk.Frame(self, bg=UIStyles.CARD_BG, highlightbackground=UIStyles.BORDER, highlightthickness=1)
        form_frame.pack(fill="x", padx=40, pady=10)

        fields = [("Username:", "username"), ("Password:", "password"),
                  ("Full Name:", "full_name")]
        self.entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(form_frame, text=label, font=("Segoe UI", 10),
                     bg=UIStyles.CARD_BG).grid(row=i, column=0, sticky="w", padx=10, pady=5)
            entry = ttk.Entry(form_frame, font=("Segoe UI", 10))
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")
            self.entries[key] = entry

        tk.Label(form_frame, text="Role:", font=("Segoe UI", 10),
                 bg=UIStyles.CARD_BG).grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.role_combo = ttk.Combobox(form_frame, state="readonly", font=("Segoe UI", 10))
        self.role_combo.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        self._load_roles()

        self.active_var = tk.BooleanVar(value=True)
        tk.Checkbutton(form_frame, text="Activo", variable=self.active_var,
                       bg=UIStyles.CARD_BG, font=("Segoe UI", 10)).grid(row=4, column=0, columnspan=2, pady=10)

        btn_frame = tk.Frame(self, bg=UIStyles.BG_LIGHT)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Guardar", bg=UIStyles.PRIMARY, fg="white",
                  font=("Segoe UI", 10, "bold"), relief="flat", padx=20,
                  command=self._save_user).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Actualizar", bg=UIStyles.CARD_ORANGE, fg="white",
                  font=("Segoe UI", 10, "bold"), relief="flat", padx=20,
                  command=self._update_user).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Eliminar", bg=UIStyles.CARD_RED, fg="white",
                  font=("Segoe UI", 10, "bold"), relief="flat", padx=20,
                  command=self._delete_user).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Desactivar", bg=UIStyles.TEXT_SECONDARY, fg="white",
                  font=("Segoe UI", 10, "bold"), relief="flat", padx=20,
                  command=self._deactivate_user).pack(side="left", padx=5)

        self.tree = ttk.Treeview(self, columns=("id", "username", "full_name", "role", "active"),
                                 show="headings", height=15)
        self.tree.heading("id", text="ID")
        self.tree.heading("username", text="Username")
        self.tree.heading("full_name", text="Full Name")
        self.tree.heading("role", text="Role")
        self.tree.heading("active", text="Active")
        self.tree.column("id", width=50)
        self.tree.column("username", width=120)
        self.tree.column("full_name", width=200)
        self.tree.column("role", width=100)
        self.tree.column("active", width=80)
        self.tree.pack(fill="both", expand=True, padx=40, pady=10)
        self.tree.bind("<ButtonRelease-1>", self._on_tree_select)

        self._refresh_table()

    def _load_roles(self):
        roles = self.role_service.get_all()
        self.roles_map = {r.name: r.role_id for r in roles}
        self.role_combo["values"] = list(self.roles_map.keys())
        if self.roles_map:
            self.role_combo.current(0)

    def _save_user(self):
        data = {k: v.get() for k, v in self.entries.items()}
        role_name = self.role_combo.get()
        if not all(data.values()) or not role_name:
            messagebox.showwarning("Campos incompletos", "Todos los campos son obligatorios")
            return
        data["role_id"] = self.roles_map[role_name]
        data["active"] = self.active_var.get()
        self.user_service.create(**data)
        messagebox.showinfo("Éxito", "Usuario guardado correctamente")
        self._clear_form()
        self._refresh_table()

    def _update_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Seleccionar", "Seleccione un usuario")
            return
        item = self.tree.item(selected[0])
        user_id = int(item["values"][0])
        data = {k: v.get() for k, v in self.entries.items() if v.get()}
        role_name = self.role_combo.get()
        if role_name:
            data["role_id"] = self.roles_map[role_name]
        data["active"] = self.active_var.get()
        self.user_service.update(user_id, **data)
        messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
        self._refresh_table()

    def _delete_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Seleccionar", "Seleccione un usuario")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar usuario?"):
            item = self.tree.item(selected[0])
            self.user_service.delete(int(item["values"][0]))
            self._refresh_table()

    def _deactivate_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Seleccionar", "Seleccione un usuario")
            return
        item = self.tree.item(selected[0])
        self.user_service.deactivate(int(item["values"][0]))
        messagebox.showinfo("Éxito", "Usuario desactivado correctamente")
        self._refresh_table()

    def _on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        vals = item["values"]
        self.entries["username"].delete(0, "end")
        self.entries["username"].insert(0, vals[1])
        self.entries["full_name"].delete(0, "end")
        self.entries["full_name"].insert(0, vals[2])
        self.active_var.set(vals[4])

    def _clear_form(self):
        for e in self.entries.values():
            e.delete(0, "end")
        self.active_var.set(True)

    def _refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        users = self.user_service.get_all()
        roles = {r.role_id: r.name for r in self.role_service.get_all()}
        for u in users:
            self.tree.insert("", "end", values=(
                u.user_id, u.username, u.full_name,
                roles.get(u.role_id, ""), "Sí" if u.active else "No"))
