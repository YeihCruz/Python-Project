import tkinter as tk
from tkinter import ttk, messagebox
from src.services.user_service import UserService
from src.ui.ui_styles import UIStyles
from src.ui.ui_scaling import UIScale


class LoginView(tk.Toplevel):
    def __init__(self, master, on_success=None):
        super().__init__(master)
        self.on_success = on_success
        self.user_service = UserService()
        self.title("Sistema de Seguros - Inicio de Sesión")
        self.resizable(True, True)
        self.minsize(UIScale.px(400), UIScale.px(520))
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        w = UIScale.px(440)
        h = UIScale.px(560)
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")
        self.configure(bg="#EBEEF5")

        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_ui(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        outer = tk.Frame(self, bg="#EBEEF5")
        outer.grid(row=0, column=0, sticky="nsew")
        outer.grid_rowconfigure(0, weight=1)
        outer.grid_columnconfigure(0, weight=1)

        card = tk.Frame(outer, bg=UIStyles.CARD_BG,
                        highlightbackground="#D2D7E1", highlightthickness=1)
        card.grid(row=0, column=0)

        pad = UIScale.px
        tk.Label(card, text="Sistema de Seguros",
                 font=("Segoe UI", UIScale.font(20), "bold"),
                 fg=UIStyles.TEXT_PRIMARY, bg=UIStyles.CARD_BG
                 ).pack(pady=(pad(50), pad(5)))

        tk.Label(card, text="Ingrese sus credenciales para acceder",
                 font=("Segoe UI", UIScale.font(11)),
                 fg=UIStyles.TEXT_SECONDARY, bg=UIStyles.CARD_BG
                 ).pack(pady=(0, pad(35)))

        tk.Label(card, text="Usuario", font=("Segoe UI", UIScale.font(11), "bold"),
                 fg=UIStyles.TEXT_PRIMARY, bg=UIStyles.CARD_BG
                 ).pack(anchor="w", padx=pad(45))
        self.txt_username = ttk.Entry(card, font=("Segoe UI", UIScale.font(12)))
        self.txt_username.pack(fill="x", padx=pad(45), pady=(pad(5), pad(18)))

        tk.Label(card, text="Contraseña", font=("Segoe UI", UIScale.font(11), "bold"),
                 fg=UIStyles.TEXT_PRIMARY, bg=UIStyles.CARD_BG
                 ).pack(anchor="w", padx=pad(45))
        self.txt_password = ttk.Entry(card, font=("Segoe UI", UIScale.font(12)), show="*")
        self.txt_password.pack(fill="x", padx=pad(45), pady=(pad(5), pad(30)))

        btn_frame = tk.Frame(card, bg=UIStyles.CARD_BG)
        btn_frame.pack(pady=pad(15))

        self.btn_login = tk.Button(btn_frame, text="Ingresar",
                                   bg=UIStyles.PRIMARY, fg="white",
                                   font=("Segoe UI", UIScale.font(11), "bold"),
                                   relief="flat", padx=pad(35), pady=pad(10),
                                   command=self._perform_login)
        self.btn_login.pack(side="left", padx=pad(8))

        self.btn_clear = tk.Button(btn_frame, text="Limpiar",
                                   bg=UIStyles.CARD_BG, fg=UIStyles.TEXT_SECONDARY,
                                   font=("Segoe UI", UIScale.font(11)),
                                   relief="solid", bd=1, padx=pad(35), pady=pad(10),
                                   command=self._clear_fields)
        self.btn_clear.pack(side="left", padx=pad(8))

        self.txt_username.focus()
        self.bind("<Return>", lambda e: self._perform_login())
        self.txt_password.bind("<Return>", lambda e: self._perform_login())

    def _perform_login(self):
        username = self.txt_username.get().strip()
        password = self.txt_password.get()

        if not username or not password:
            messagebox.showwarning("Campos incompletos",
                                   "Complete todos los campos necesarios para iniciar sesión")
            return

        user = self.user_service.login(username, password)
        if user is None:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
            self.txt_password.delete(0, "end")
            self.txt_password.focus()
            return

        messagebox.showinfo("Éxito", "Ha iniciado sesión con éxito")
        self.destroy()
        if self.on_success:
            self.on_success(user)

    def _on_close(self):
        self.master.destroy()

    def _clear_fields(self):
        self.txt_username.delete(0, "end")
        self.txt_password.delete(0, "end")
        self.txt_username.focus()
