import ctypes
import tkinter as tk
from tkinter import ttk


class UIScale:
    _dpi_factor = 1.0
    _initialized = False

    @classmethod
    def _set_dpi_awareness(cls):
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception:
                pass

    @classmethod
    def initialize(cls, root: tk.Tk):
        if cls._initialized:
            return
        cls._set_dpi_awareness()
        try:
            dpi = root.winfo_fpixels('1i')
            cls._dpi_factor = max(1.0, dpi / 96.0)
        except Exception:
            cls._dpi_factor = 1.0
        cls._initialized = True

    @classmethod
    def font(cls, size: int) -> int:
        return max(size, round(size * cls._dpi_factor))

    @classmethod
    def px(cls, value: int) -> int:
        return max(1, round(value * cls._dpi_factor))

    @classmethod
    def factor(cls) -> float:
        return cls._dpi_factor

    @classmethod
    def configure_tree_columns(cls, tree: ttk.Treeview, col_config: list):
        tree.update_idletasks()
        available = tree.winfo_width() - 20
        if available <= 50:
            return
        total = sum(w for _, _, w in col_config)
        if available > total * 1.2:
            ratios = [w / total for _, _, w in col_config]
            for (col_key, _, _), ratio in zip(col_config, ratios):
                new_w = max(cls.px(50), int(available * ratio))
                tree.column(col_key, width=new_w)
