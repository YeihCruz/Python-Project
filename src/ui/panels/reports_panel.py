import tkinter as tk
from tkinter import ttk
from src.ui.ui_styles import UIStyles
from src.services.reports_service import ReportsService
from src.ui.ui_scaling import UIScale


class ReportsPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=UIStyles.BG_LIGHT)
        self.reports_service = ReportsService()

        tk.Label(self, text="Reportes",
                 font=("Segoe UI", UIScale.font(18), "bold"),
                 fg=UIStyles.TEXT_PRIMARY, bg=UIStyles.BG_LIGHT
                 ).pack(pady=(UIScale.px(20), UIScale.px(10)))

        self._build_button_bar()
        self.content = tk.Frame(self, bg=UIStyles.BG_LIGHT)
        self.content.pack(fill="both", expand=True, padx=UIScale.px(40), pady=UIScale.px(10))
        self.content.grid_rowconfigure(0, weight=1)
        self.content.grid_columnconfigure(0, weight=1)

        self._current_view = None
        self._show_placeholder()

    def _build_button_bar(self):
        p = UIScale.px
        bar_bg = tk.Frame(self, bg=UIStyles.BG_LIGHT)
        bar_bg.pack(fill="x", padx=p(40))
        bar_bg.grid_columnconfigure(0, weight=1)

        canvas = tk.Canvas(bar_bg, bg=UIStyles.BG_LIGHT, highlightthickness=0, height=p(40))
        canvas.grid(row=0, column=0, sticky="ew")

        hsb = ttk.Scrollbar(bar_bg, orient="horizontal", command=canvas.xview)
        hsb.grid(row=1, column=0, sticky="ew")
        canvas.configure(xscrollcommand=hsb.set)

        inner = tk.Frame(canvas, bg=UIStyles.BG_LIGHT)
        canvas.create_window((0, 0), window=inner, anchor="nw")

        reports = [
            ("Clientes", self._show_clients),
            ("Pólizas", self._show_policies),
            ("Reclamos", self._show_claims),
            ("Re-Aseguradoras", self._show_reinsurers),
            ("Pólizas Vencidas", self._show_expired),
            ("Pólizas Canceladas", self._show_cancelled),
            ("Pólizas Activas", self._show_policy_summary),
            ("Resumen Reclamos", self._show_claim_summary),
            ("Ingresos Mensuales", self._show_monthly_income),
            ("Reclamos Aprobados", self._show_approved),
            ("Reclamos Rechazados", self._show_rejected),
            ("Agencia", self._show_agency),
        ]

        for text, cmd in reports:
            tk.Button(inner, text=text, font=("Segoe UI", UIScale.font(9)),
                      bg=UIStyles.CARD_BG, relief="solid", bd=1,
                      padx=p(10), pady=p(4), command=cmd
                      ).pack(side="left", padx=p(3), pady=p(3))

        inner.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.config(height=inner.winfo_reqheight())

    def _clear(self):
        if self._current_view is not None:
            self._current_view.pack_forget()
            self._current_view.destroy()
            self._current_view = None

    def _show_placeholder(self):
        self._clear()
        self._current_view = tk.Frame(self.content, bg=UIStyles.BG_LIGHT)
        self._current_view.grid(row=0, column=0, sticky="nsew")
        tk.Label(self._current_view,
                 text="Seleccione un reporte del menú superior",
                 font=("Segoe UI", UIScale.font(12)),
                 fg=UIStyles.TEXT_SECONDARY, bg=UIStyles.BG_LIGHT
                 ).pack(expand=True)

    def _show_table(self, title, columns, rows, count_text=None):
        self._clear()
        container = tk.Frame(self.content, bg=UIStyles.BG_LIGHT)
        container.grid(row=0, column=0, sticky="nsew")
        container.grid_rowconfigure(1, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self._current_view = container

        p = UIScale.px
        if title:
            tk.Label(container, text=title,
                     font=("Segoe UI", UIScale.font(14), "bold"),
                     fg=UIStyles.TEXT_PRIMARY, bg=UIStyles.BG_LIGHT
                     ).grid(row=0, column=0, sticky="w", pady=(0, p(10)))

        table_bg = tk.Frame(container, bg=UIStyles.CARD_BG,
                            highlightbackground=UIStyles.BORDER, highlightthickness=1)
        table_bg.grid(row=1, column=0, sticky="nsew")
        table_bg.grid_rowconfigure(0, weight=1)
        table_bg.grid_columnconfigure(0, weight=1)

        cols = [c[0] for c in columns]
        headings = [c[1] for c in columns]
        widths = [c[2] for c in columns]
        anchors = [c[3] if len(c) > 3 else "center" for c in columns]

        style_name = f"Report_{id(self)}.Treeview"
        style_heading = f"Report_{id(self)}.Treeview.Heading"

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(style_name,
                        font=("Segoe UI", UIScale.font(10)),
                        rowheight=UIScale.px(30),
                        foreground=UIStyles.TEXT_PRIMARY)
        style.configure(style_heading,
                        font=("Segoe UI", UIScale.font(10), "bold"),
                        background=UIStyles.PRIMARY,
                        foreground="white",
                        relief="flat")
        style.map(style_heading, background=[("active", UIStyles.PRIMARY_DARK)])
        style.map(style_name,
                  background=[("selected", "#D0E0F5")],
                  foreground=[("selected", UIStyles.TEXT_PRIMARY)])

        tree = ttk.Treeview(table_bg, columns=cols, show="headings",
                            style=style_name)
        tree.grid(row=0, column=0, sticky="nsew")

        for col_key, col_text, col_width, col_anchor in zip(cols, headings, widths, anchors):
            tree.heading(col_key, text=col_text)
            tree.column(col_key, width=UIScale.px(col_width), minwidth=UIScale.px(50), anchor=col_anchor)

        vsb = ttk.Scrollbar(table_bg, orient="vertical", command=tree.yview)
        vsb.grid(row=0, column=1, sticky="ns")
        hsb = ttk.Scrollbar(table_bg, orient="horizontal", command=tree.xview)
        hsb.grid(row=1, column=0, sticky="ew")
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        for i, row in enumerate(rows):
            tag = "even" if i % 2 == 0 else "odd"
            tree.insert("", "end", values=row, tags=(tag,))
        tree.tag_configure("even", background="#F0F4FA")
        tree.tag_configure("odd", background=UIStyles.CARD_BG)

        def _on_tree_map(evt):
            tree.update_idletasks()
            avail = tree.winfo_width() - 20

            if avail > 50:
                total = sum(widths)

                for col, ratio in zip(columns, [w / total for w in widths]):
                    ck = col[0]

                    new_w = max(UIScale.px(50), int(avail * ratio))
                    tree.column(ck, width=new_w)

        tree.bind("<Map>", _on_tree_map)

        if count_text:
            tk.Label(container, text=count_text,
                     font=("Segoe UI", UIScale.font(10)),
                     fg=UIStyles.TEXT_SECONDARY, bg=UIStyles.BG_LIGHT
                     ).grid(row=2, column=0, sticky="e", pady=(p(5), 0))

    def _show_clients(self):
        data = self.reports_service.get_client_details_report()
        columns = [
            ("id", "ID", 40, "center"),
            ("first_name", "Nombre", 130, "w"),
            ("last_name", "Apellidos", 160, "w"),
            ("id_num", "Cédula", 120, "center"),
            ("age", "Edad", 50, "center"),
            ("gender", "Sexo", 90, "center"),
            ("country", "País", 120, "w"),
            ("phone", "Teléfono", 120, "center"),
            ("email", "Correo Electrónico", 180, "w"),
            ("address", "Dirección", 200, "w"),
            ("policies", "Pólizas", 65, "center"),
            ("premiums", "Primas", 100, "e"),
        ]
        rows = [
            (
                r["client_id"], r["first_name"], r["last_name"],
                r["identification_number"], r["age"], r["gender"],
                r["country"], r["phone"], r["email"], r["address"],
                r["active_policies"], f'${r["total_premiums"]:,.2f}',
            )
            for r in data
        ]
        self._show_table("Clientes del Sistema", columns, rows,
                         f"Total: {len(data)} clientes")

    def _show_policies(self):
        data = self.reports_service.get_policies_report()
        columns = [
            ("num", "No.", 60, "center"),
            ("type", "Tipo Seguro", 110, "w"),
            ("client", "Cliente", 180, "w"),
            ("start", "Inicio", 100, "center"),
            ("end", "Vencimiento", 100, "center"),
            ("premium", "Prima Mensual", 110, "e"),
            ("amount", "Monto Asegurado", 120, "e"),
            ("status", "Estado", 90, "center"),
        ]
        rows = [
            (
                r.policy_number, r.insurance_type, r.client_name,
                r.start_date, r.end_date,
                f'${r.monthly_premium:,.2f}',
                f'${r.insured_amount:,.2f}',
                r.policy_status,
            )
            for r in data
        ]
        self._show_table("Pólizas del Sistema", columns, rows,
                         f"Total: {len(data)} pólizas")

    def _show_claims(self):
        data = self.reports_service.get_claims_report()
        columns = [
            ("cn", "Reclamo", 70, "center"),
            ("client", "Cliente", 170, "w"),
            ("pn", "Póliza", 60, "center"),
            ("type", "Tipo", 120, "w"),
            ("date", "Fecha", 100, "center"),
            ("claimed", "Reclamado", 100, "e"),
            ("comp", "Compensado", 100, "e"),
            ("status", "Estado", 90, "center"),
        ]
        rows = [
            (
                r.claim_number, r.client_name, r.policy_number,
                r.claim_type, r.incident_date,
                f'${r.claimed_amount:,.2f}',
                f'${r.compensated_amount:,.2f}' if r.compensated_amount else "$0.00",
                r.claim_status,
            )
            for r in data
        ]
        self._show_table("Reclamos del Sistema", columns, rows,
                         f"Total: {len(data)} reclamos")

    def _show_reinsurers(self):
        data = self.reports_service.get_reinsurers_report()
        columns = [
            ("name", "Reaseguradora", 220, "w"),
            ("country", "País", 130, "w"),
            ("rtype", "Tipo Reaseguro", 140, "w"),
            ("itype", "Tipo Seguro", 120, "w"),
            ("pct", "Participación", 100, "e"),
        ]
        rows = [
            (
                r.reinsurer_name, r.country_name, r.reinsurance_type,
                r.insurance_type,
                f"{r.participation_percentage:.2f}%",
            )
            for r in data
        ]
        self._show_table("Reaseguradoras", columns, rows,
                         f"Total: {len(data)} registros")

    def _show_expired(self):
        data = self.reports_service.get_expired_policies_report()
        columns = [
            ("num", "No.", 60, "center"),
            ("client", "Cliente", 180, "w"),
            ("type", "Tipo Seguro", 130, "w"),
            ("start", "Inicio", 100, "center"),
            ("end", "Vencimiento", 100, "center"),
            ("amount", "Monto Asegurado", 120, "e"),
        ]
        rows = [
            (
                r.policy_number, r.client_name, r.insurance_type,
                r.start_date, r.end_date,
                f'${r.insured_amount:,.2f}',
            )
            for r in data
        ]
        self._show_table("Pólizas Vencidas", columns, rows,
                         f"Total: {len(data)} pólizas vencidas")

    def _show_cancelled(self):
        data = self.reports_service.get_cancelled_policies_report()
        columns = [
            ("client", "Cliente", 200, "w"),
            ("id_num", "Cédula", 130, "center"),
            ("count", "Canceladas", 90, "center"),
            ("reasons", "Razones", 400, "w"),
        ]
        rows = [
            (
                r.client_name, r.identification_number,
                r.cancelled_policies, r.cancellation_reasons,
            )
            for r in data
        ]
        self._show_table("Pólizas Canceladas", columns, rows,
                         f"Total: {len(data)} clientes con cancelaciones")

    def _show_policy_summary(self):
        data = self.reports_service.get_policy_summary_report()
        columns = [
            ("type", "Tipo de Seguro", 180, "w"),
            ("count", "Pólizas Activas", 110, "center"),
            ("premium", "Total Primas Mensuales", 160, "e"),
            ("amount", "Total Monto Asegurado", 170, "e"),
        ]
        rows = [
            (
                r.insurance_type, r.active_policies,
                f'${r.total_monthly_premium:,.2f}',
                f'${r.total_insured_amount:,.2f}',
            )
            for r in data
        ]
        self._show_table("Resumen de Pólizas Activas", columns, rows)

    def _show_claim_summary(self):
        data = self.reports_service.get_claim_status_summary_report()
        columns = [
            ("status", "Estado", 140, "w"),
            ("count", "Cantidad", 80, "center"),
            ("claimed", "Total Reclamado", 140, "e"),
            ("comp", "Total Compensado", 140, "e"),
        ]
        rows = [
            (
                r.claim_status, r.total_claims,
                f'${r.total_claimed_amount:,.2f}',
                f'${r.total_compensated_amount:,.2f}',
            )
            for r in data
        ]
        self._show_table("Resumen de Reclamos por Estado", columns, rows)

    def _show_monthly_income(self):
        data = self.reports_service.get_monthly_income_report()
        columns = [
            ("month", "Mes", 200, "w"),
            ("income", "Ingreso Mensual", 150, "e"),
        ]
        rows = [
            (r.month_name, f'${r.monthly_income:,.2f}')
            for r in data
        ]
        self._show_table("Ingresos Mensuales por Primas", columns, rows)

    def _show_approved(self):
        data = self.reports_service.get_approved_claims_report()
        columns = [
            ("client", "Cliente", 200, "w"),
            ("id_num", "Cédula", 130, "center"),
            ("count", "Reclamos Aprobados", 130, "center"),
            ("comp", "Total Compensado", 140, "e"),
        ]
        rows = [
            (
                r.client_name, r.identification_number,
                r.approved_claims,
                f'${r.total_compensated_amount:,.2f}',
            )
            for r in data
        ]
        self._show_table("Reclamos Aprobados", columns, rows,
                         f"Total: {len(data)} clientes")

    def _show_rejected(self):
        data = self.reports_service.get_rejected_claims_report()
        columns = [
            ("client", "Cliente", 200, "w"),
            ("id_num", "Cédula", 130, "center"),
            ("count", "Reclamos Rechazados", 140, "center"),
            ("reason", "Motivo", 300, "w"),
        ]
        rows = [
            (
                r.client_name, r.identification_number,
                r.rejected_claims, r.rejection_reason,
            )
            for r in data
        ]
        self._show_table("Reclamos Rechazados", columns, rows,
                         f"Total: {len(data)} clientes")

    def _show_agency(self):
        data = self.reports_service.get_agency_report()
        if not data:
            self._show_table("Agencia", [("info", "Sin datos", 200, "w")], [])
            return
        r = data[0]
        columns = [
            ("field", "", 180, "w"),
            ("value", "", 400, "w"),
        ]
        rows = [
            ("Nombre", r.name),
            ("Dirección", r.address),
            ("Teléfono", r.phone),
            ("Correo Electrónico", r.email),
            ("Director General", r.general_director),
            ("Gerente de Seguros", r.insurance_manager),
            ("Gerente de Reclamos", r.claims_manager),
        ]
        self._show_table("Agencia", columns, rows)
