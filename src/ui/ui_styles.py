import tkinter as tk
from tkinter import ttk


class UIStyles:
    PRIMARY = "#1E64C8"
    PRIMARY_DARK = "#1450AA"
    PRIMARY_LIGHT = "#DCEBFF"
    BG_LIGHT = "#F2F4F8"
    CARD_BG = "#FFFFFF"
    TEXT_PRIMARY = "#1E1E23"
    TEXT_SECONDARY = "#787D87"
    TEXT_MUTED = "#AAAFB9"
    BORDER = "#E1E4EB"
    BORDER_LIGHT = "#EEF0F5"

    SIDEBAR_BG = "#161E2D"
    SIDEBAR_HOVER = "#202A3C"
    SIDEBAR_SELECTED = "#1E64C8"
    SIDEBAR_TEXT = "#C3C8D2"
    SIDEBAR_BRAND_BG = "#101623"
    SIDEBAR_DIVIDER = "#283244"

    CARD_BLUE = "#1E64C8"
    CARD_GREEN = "#28A050"
    CARD_ORANGE = "#DC8C1E"
    CARD_RED = "#C83C3C"
    CARD_PURPLE = "#8246BE"
    CARD_TEAL = "#149696"

    @staticmethod
    def configure_ttk_styles():
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Primary.TButton",
                        background=UIStyles.PRIMARY,
                        foreground="white",
                        borderwidth=0,
                        focuscolor="none",
                        font=("Segoe UI", 10, "bold"))
        style.map("Primary.TButton",
                  background=[("active", UIStyles.PRIMARY_DARK)])

        style.configure("Secondary.TButton",
                        background=UIStyles.CARD_BG,
                        foreground=UIStyles.TEXT_SECONDARY,
                        borderwidth=1,
                        font=("Segoe UI", 10))
        style.map("Secondary.TButton",
                  background=[("active", "#F5F5F7")])

        style.configure("Sidebar.TButton",
                        background=UIStyles.SIDEBAR_BG,
                        foreground=UIStyles.SIDEBAR_TEXT,
                        borderwidth=0,
                        font=("Segoe UI", 11),
                        anchor="w")
        style.map("Sidebar.TButton",
                  background=[("active", UIStyles.SIDEBAR_HOVER)])

        style.configure("TLabel",
                        background=UIStyles.BG_LIGHT,
                        foreground=UIStyles.TEXT_PRIMARY,
                        font=("Segoe UI", 10))

        style.configure("Card.TFrame",
                        background=UIStyles.CARD_BG)
