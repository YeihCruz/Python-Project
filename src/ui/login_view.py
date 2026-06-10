import tkinter as tk
from tkinter import ttk, messagebox
from src.services.user_service import UserService
from src.ui.ui_styles import UIStyles
from src.ui.home_view import HomeView


class LoginView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.user_service = UserService()
        self.title("Sistema de Seguros - Inicio de Sesión")
        self.geometry("400x520")
        self.resizable(False, False)
        self.configure(bg="#EBEEF5")

        self._build_ui()

    def _build_ui(self):
        card = tk.Frame(self, bg=UIStyles.CARD_BG, highlightbackground="#D2D7E1", highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center", width=360, height=460)

        title = tk.Label(card, text="Sistema de Seguros",
                         font=("Segoe UI", 18, "bold"),
                         fg=UIStyles.TEXT_PRIMARY, bg=UIStyles.CARD_BG)
        title.pack(pady=(40, 5))

        subtitle = tk.Label(card, text="Ingrese sus credenciales para acceder",
                            font=("Segoe UI", 10),
                            fg=UIStyles.TEXT_SECONDARY, bg=UIStyles.CARD_BG)
        subtitle.pack(pady=(0, 30))

        tk.Label(card, text="Usuario", font=("Segoe UI", 10, "bold"),
                 fg=UIStyles.TEXT_PRIMARY, bg=UIStyles.CARD_BG).pack(anchor="w", padx=40)
        self.txt_username = ttk.Entry(card, font=("Segoe UI", 11))
        self.txt_username.pack(fill="x", padx=40, pady=(5, 15))

        tk.Label(card, text="Contraseña", font=("Segoe UI", 10, "bold"),
                 fg=UIStyles.TEXT_PRIMARY, bg=UIStyles.CARD_BG).pack(anchor="w", padx=40)
        self.txt_password = ttk.Entry(card, font=("Segoe UI", 11), show="*")
        self.txt_password.pack(fill="x", padx=40, pady=(5, 25))

        btn_frame = tk.Frame(card, bg=UIStyles.CARD_BG)
        btn_frame.pack(pady=10)

        btn_login = tk.Button(btn_frame, text="Ingresar",
                              bg=UIStyles.PRIMARY, fg="white",
                              font=("Segoe UI", 10, "bold"),
                              relief="flat", padx=30, pady=8,
                              command=self._perform_login)
        btn_login.pack(side="left", padx=5)

        btn_clear = tk.Button(btn_frame, text="Limpiar",
                              bg=UIStyles.CARD_BG, fg=UIStyles.TEXT_SECONDARY,
                              font=("Segoe UI", 10),
                              relief="solid", bd=1, padx=30, pady=8,
                              command=self._clear_fields)
        btn_clear.pack(side="left", padx=5)

        self.txt_username.focus()
        self.bind("<Return>", lambda e: self._perform_login())
        self.txt_password.bind("<Return>", lambda e: self._perform_login())

    def _perform_login(self):
        username = self.txt_username.get().strip()
        password = self.txt_password.get()

        if not username or not password:
            messagebox.showwarning("Campos incompletos", "Complete todos los campos necesarios para iniciar sesión")
            return

        user = self.user_service.login(username, password)
        if user is None:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
            self.txt_password.delete(0, "end")
            self.txt_password.focus()
            return

        messagebox.showinfo("Éxito", "Ha iniciado sesión con éxito")
        self.destroy()
        HomeView(user).run()

    def _clear_fields(self):
        self.txt_username.delete(0, "end")
        self.txt_password.delete(0, "end")
        self.txt_username.focus()
