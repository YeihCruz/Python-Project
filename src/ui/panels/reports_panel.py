import tkinter as tk
from tkinter import ttk, scrolledtext
from src.ui.ui_styles import UIStyles
from src.services.reports_service import ReportsService


class ReportsPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=UIStyles.BG_LIGHT)
        self.reports_service = ReportsService()

        tk.Label(self, text="Reportes",
                 font=("Segoe UI", 18, "bold"),
                 fg=UIStyles.TEXT_PRIMARY, bg=UIStyles.BG_LIGHT).pack(pady=20)

        btn_frame = tk.Frame(self, bg=UIStyles.BG_LIGHT)
        btn_frame.pack(pady=10)

        reports = [
            ("Clientes", self._show_clients),
            ("Pólizas", self._show_policies),
            ("Reclamos", self._show_claims),
            ("Reaseguradoras", self._show_reinsurers),
            ("Pólizas Vencidas", self._show_expired),
            ("Pólizas Canceladas", self._show_cancelled),
            ("Resumen Pólizas", self._show_policy_summary),
            ("Resumen Reclamos", self._show_claim_summary),
            ("Ingresos Mensuales", self._show_monthly_income),
            ("Reclamos Aprobados", self._show_approved),
            ("Reclamos Rechazados", self._show_rejected),
            ("Agencia", self._show_agency),
        ]

        for text, cmd in reports:
            tk.Button(btn_frame, text=text, font=("Segoe UI", 9),
                      bg=UIStyles.CARD_BG, relief="solid", bd=1,
                      padx=10, pady=4, command=cmd).pack(side="left", padx=3, pady=3)

        self.text_area = scrolledtext.ScrolledText(self, wrap="word", font=("Courier New", 10))
        self.text_area.pack(fill="both", expand=True, padx=40, pady=10)

    def _show_clients(self):
        self.text_area.delete(1.0, "end")
        self.text_area.insert("end", str(self.reports_service.get_clients_report()))

    def _show_policies(self):
        self.text_area.delete(1.0, "end")
        self.text_area.insert("end", str(self.reports_service.get_policies_report()))

    def _show_claims(self):
        self.text_area.delete(1.0, "end")
        self.text_area.insert("end", str(self.reports_service.get_claims_report()))

    def _show_reinsurers(self):
        self.text_area.delete(1.0, "end")
        self.text_area.insert("end", str(self.reports_service.get_reinsurers_report()))

    def _show_expired(self):
        self.text_area.delete(1.0, "end")
        self.text_area.insert("end", str(self.reports_service.get_expired_policies_report()))

    def _show_cancelled(self):
        self.text_area.delete(1.0, "end")
        self.text_area.insert("end", str(self.reports_service.get_cancelled_policies_report()))

    def _show_policy_summary(self):
        self.text_area.delete(1.0, "end")
        self.text_area.insert("end", str(self.reports_service.get_policy_summary_report()))

    def _show_claim_summary(self):
        self.text_area.delete(1.0, "end")
        self.text_area.insert("end", str(self.reports_service.get_claim_status_summary_report()))

    def _show_monthly_income(self):
        self.text_area.delete(1.0, "end")
        self.text_area.insert("end", str(self.reports_service.get_monthly_income_report()))

    def _show_approved(self):
        self.text_area.delete(1.0, "end")
        self.text_area.insert("end", str(self.reports_service.get_approved_claims_report()))

    def _show_rejected(self):
        self.text_area.delete(1.0, "end")
        self.text_area.insert("end", str(self.reports_service.get_rejected_claims_report()))

    def _show_agency(self):
        self.text_area.delete(1.0, "end")
        self.text_area.insert("end", str(self.reports_service.get_agency_report()))
