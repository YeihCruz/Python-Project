import tkinter as tk
from tkinter import ttk, messagebox
from src.ui.ui_styles import UIStyles
from src.services.user_service import UserService
from src.services.role_service import RoleService
from src.services.exceptions import ServiceError
from src.ui.ui_scaling import UIScale


class UsersPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=UIStyles.BG_LIGHT)
        self.user_service = UserService()
        self.role_service = RoleService()
        tk.Label(self, text="Gestión de Usuarios",
                 font=("Segoe UI", UIScale.font(18), "bold"),
                 fg=UIStyles.TEXT_PRIMARY, bg=UIStyles.BG_LIGHT
                 ).pack(pady=(UIScale.px(20), UIScale.px(10)))

        p = UIScale.px
        form_frame = tk.Frame(self, bg=UIStyles.CARD_BG,
                              highlightbackground=UIStyles.BORDER, highlightthickness=1)
        form_frame.pack(fill="x", padx=p(40), pady=p(10))
        form_frame.grid_columnconfigure(1, weight=1)

        fields = [("Usuario:", "username"), ("Contraseña:", "password"),
                  ("Nombre Completo:", "full_name")]
        self.entries = {}
        for i, (label, key) in enumerate(fields):
            tk.Label(form_frame, text=label, font=("Segoe UI", UIScale.font(10)),
                     bg=UIStyles.CARD_BG).grid(row=i, column=0, sticky="w", padx=p(10), pady=p(5))

            if key == "password":
                entry = ttk.Entry(form_frame,font=("Segoe UI", UIScale.font(10)))
            else:
                entry = ttk.Entry(form_frame,font=("Segoe UI", UIScale.font(10)))

            entry.grid(row=i, column=1, padx=p(10), pady=p(5), sticky="ew")
            self.entries[key] = entry

        tk.Label(form_frame, text="Rol:", font=("Segoe UI", UIScale.font(10)),
                 bg=UIStyles.CARD_BG).grid(row=3, column=0, sticky="w", padx=p(10), pady=p(5))
        self.role_combo = ttk.Combobox(form_frame, state="readonly",
                                       font=("Segoe UI", UIScale.font(10)))
        self.role_combo.grid(row=3, column=1, padx=p(10), pady=p(5), sticky="ew")
        self._load_roles()

        self.active_var = tk.BooleanVar(value=True)
        tk.Checkbutton(form_frame, text="Activo", variable=self.active_var,
                       bg=UIStyles.CARD_BG, font=("Segoe UI", UIScale.font(10))
                       ).grid(row=4, column=0, columnspan=2, pady=p(10))

        btn_frame = tk.Frame(self, bg=UIStyles.BG_LIGHT)
        btn_frame.pack(pady=p(10))
        tk.Button(btn_frame, text="Guardar", bg=UIStyles.PRIMARY, fg="white",
                  font=("Segoe UI", UIScale.font(10), "bold"), relief="flat", padx=p(20),
                  command=self._save_user).pack(side="left", padx=p(5))
        tk.Button(btn_frame, text="Actualizar", bg=UIStyles.CARD_ORANGE, fg="white",
                  font=("Segoe UI", UIScale.font(10), "bold"), relief="flat", padx=p(20),
                  command=self._update_user).pack(side="left", padx=p(5))
        tk.Button(btn_frame, text="Eliminar", bg=UIStyles.CARD_RED, fg="white",
                  font=("Segoe UI", UIScale.font(10), "bold"), relief="flat", padx=p(20),
                  command=self._delete_user).pack(side="left", padx=p(5))
        tk.Button(btn_frame, text="Desactivar", bg=UIStyles.CARD_GREEN, fg="white",
                  font=("Segoe UI", UIScale.font(10), "bold"), relief="flat", padx=p(20),
                  command=self._deactivate_user).pack(side="left", padx=p(5))

        tree_frame = tk.Frame(self, bg=UIStyles.BG_LIGHT)
        tree_frame.pack(fill="both", expand=True, padx=p(40), pady=p(10))
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(tree_frame, columns=("id", "username", "full_name", "role", "active"),
                                 show="headings")
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree_col_config = [
            ("id", "ID", 50), ("username", "Usuario", 130),
            ("full_name", "Nombre Completo", 200), ("role", "Rol", 110),
            ("active", "Activo", 80)
        ]
        for col, text, width in self.tree_col_config:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=UIScale.px(width))

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        vsb.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.bind("<Map>", self._on_tree_map)
        self.tree.bind("<ButtonRelease-1>", self._on_tree_select)
        self._refresh_table()

    def _on_tree_map(self, event):
        UIScale.configure_tree_columns(self.tree, self.tree_col_config)

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
        try:
            self.user_service.create(**data)
        except ServiceError as e:
            messagebox.showerror("Error", str(e))
            return
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

        data = {}

        if self.entries["username"].get():
            data["username"] = self.entries["username"].get()

        if self.entries["password"].get():
            data["password"] = self.entries["password"].get()

        if self.entries["full_name"].get():
            data["full_name"] = self.entries["full_name"].get()

        role_name = self.role_combo.get()
        if role_name and role_name in self.roles_map:
            data["role_id"] = self.roles_map[role_name]

        data["active"] = self.active_var.get()

        try:
            self.user_service.update(user_id, **data)
        except ServiceError as e:
            messagebox.showerror("Error", str(e))
            return

        messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
        self._clear_form()
        self._refresh_table()

    def _delete_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Seleccionar", "Seleccione un usuario")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar usuario?"):
            item = self.tree.item(selected[0])
            try:
                self.user_service.delete(int(item["values"][0]))
            except ServiceError as e:
                messagebox.showerror("Error", str(e))
                return
            self._clear_form()
            self._refresh_table()

    def _deactivate_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Seleccionar", "Seleccione un usuario")
            return
        item = self.tree.item(selected[0])
        try:
            self.user_service.deactivate(int(item["values"][0]))
        except ServiceError as e:
            messagebox.showerror("Error", str(e))
            return
        messagebox.showinfo("Éxito", "Usuario desactivado correctamente")
        self._refresh_table()

    def _on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        vals = item["values"]

        # ID 0 (no lo usas en form)
        username = vals[1]
        full_name = vals[2]
        role_name = vals[3]
        active = vals[4]

        # username
        self.entries["username"].delete(0, "end")
        self.entries["username"].insert(0, username)

        # full_name
        self.entries["full_name"].delete(0, "end")
        self.entries["full_name"].insert(0, full_name)

        # password (never populated — stored as irreversible hash)
        self.entries["password"].delete(0, "end")

        # role combo (ESTO TE FALTABA COMPLETO)
        if role_name in self.roles_map:
            self.role_combo.set(role_name)
        else:
            self.role_combo.set("")

        # active
        self.active_var.set(
            str(active).lower() in ("sí", "si", "true", "1")
        )

    def _clear_form(self):
        for e in self.entries.values():
            e.delete(0, "end")

        self.role_combo.set("")
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
