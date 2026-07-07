from dataclasses import dataclass
from typing import List
from sqlalchemy import text
from src.database.connection import get_db


@dataclass
class ClientReport:
    country: str = ""
    client_name: str = ""
    identification_number: str = ""
    active_policies: int = 0
    total_premiums: float = 0.0


@dataclass
class PolicyReport:
    insurance_type: str = ""
    policy_number: int = 0
    client_name: str = ""
    start_date: str = ""
    end_date: str = ""
    monthly_premium: float = 0.0
    insured_amount: float = 0.0
    policy_status: str = ""


@dataclass
class ClaimReport:
    client_name: str = ""
    policy_number: int = 0
    insurance_type: str = ""
    claim_number: int = 0
    claim_type: str = ""
    incident_date: str = ""
    claimed_amount: float = 0.0
    claim_status: str = ""
    compensated_amount: float = 0.0


@dataclass
class ReinsurerReport:
    reinsurer_name: str = ""
    country_name: str = ""
    reinsurance_type: str = ""
    insurance_type: str = ""
    participation_percentage: float = 0.0


@dataclass
class ExpiredPolicyReport:
    policy_number: int = 0
    client_name: str = ""
    insurance_type: str = ""
    start_date: str = ""
    end_date: str = ""
    insured_amount: float = 0.0


@dataclass
class CancelledPolicyReport:
    client_name: str = ""
    identification_number: str = ""
    cancelled_policies: int = 0
    cancellation_reasons: str = ""


@dataclass
class PolicySummaryReport:
    insurance_type: str = ""
    active_policies: int = 0
    total_monthly_premium: float = 0.0
    total_insured_amount: float = 0.0


@dataclass
class ClaimStatusSummaryReport:
    claim_status: str = ""
    total_claims: int = 0
    total_claimed_amount: float = 0.0
    total_compensated_amount: float = 0.0


@dataclass
class MonthlyIncomeReport:
    month_name: str = ""
    monthly_income: float = 0.0


@dataclass
class ApprovedClaimsReport:
    client_name: str = ""
    identification_number: str = ""
    approved_claims: int = 0
    total_compensated_amount: float = 0.0


@dataclass
class RejectedClaimsReport:
    client_name: str = ""
    identification_number: str = ""
    rejected_claims: int = 0
    rejection_reason: str = ""


@dataclass
class AgencyReport:
    name: str = ""
    address: str = ""
    phone: str = ""
    email: str = ""
    general_director: str = ""
    insurance_manager: str = ""
    claims_manager: str = ""


@dataclass
class ClientProfileReport:
    client_name: str = ""
    identification_number: str = ""
    phone: str = ""
    address: str = ""
    email: str = ""
    active_policies: int = 0
    total_premiums_paid: float = 0.0
    claim_number: int = 0
    incident_date: str = ""
    claimed_amount: float = 0.0
    compensated_amount: float = 0.0


@dataclass
class ReinsurerProfileReport:
    reinsurer_name: str = ""
    country: str = ""
    reinsurance_type: str = ""
    total_participation: float = 0.0


class ReportsService:
    def get_clients_report(self) -> List[ClientReport]:
        sql = text("""
            SELECT co.name, c.first_name, c.last_name,
                   c.identification_number,
                   COUNT(p.policy_number) AS active_policies,
                   COALESCE(SUM(p.monthly_premium), 0) AS total_premiums
            FROM client c
            INNER JOIN country co ON c.country_id = co.country_id
            LEFT JOIN policy p ON c.client_id = p.client_id
            LEFT JOIN policy_status ps ON p.policy_status_id = ps.policy_status_id
                AND ps.description = 'Activa'
            GROUP BY co.name, c.first_name, c.last_name, c.identification_number
            ORDER BY co.name, c.last_name, c.first_name
        """)
        with get_db() as db:
            rows = db.execute(sql).fetchall()
        reports = []
        for row in rows:
            reports.append(ClientReport(
                country=row[0], client_name=f"{row[1]} {row[2]}",
                identification_number=row[3], active_policies=row[4],
                total_premiums=float(row[5])
            ))
        return reports

    def get_policies_report(self) -> List[PolicyReport]:
        sql = text("""
            SELECT it.description, p.policy_number, c.first_name, c.last_name,
                   p.start_date, p.end_date, p.monthly_premium, p.insured_amount,
                   ps.description
            FROM policy p
            INNER JOIN client c ON p.client_id = c.client_id
            INNER JOIN insurance_type it ON p.insurance_type_id = it.insurance_type_id
            INNER JOIN policy_status ps ON p.policy_status_id = ps.policy_status_id
            ORDER BY p.policy_number
        """)
        with get_db() as db:
            rows = db.execute(sql).fetchall()
        reports = []
        for row in rows:
            reports.append(PolicyReport(
                insurance_type=row[0], policy_number=row[1],
                client_name=f"{row[2]} {row[3]}",
                start_date=str(row[4]), end_date=str(row[5]),
                monthly_premium=float(row[6]), insured_amount=float(row[7]),
                policy_status=row[8]
            ))
        return reports

    def get_claims_report(self) -> List[ClaimReport]:
        sql = text("""
            SELECT c.first_name, c.last_name, p.policy_number, it.description,
                   cl.claim_number, ct.description, cl.incident_date,
                   cl.claimed_amount, cs.description, cl.compensated_amount
            FROM claim cl
            INNER JOIN policy p ON cl.policy_number = p.policy_number
            INNER JOIN client c ON p.client_id = c.client_id
            INNER JOIN insurance_type it ON p.insurance_type_id = it.insurance_type_id
            INNER JOIN claim_type ct ON cl.claim_type_id = ct.claim_type_id
            INNER JOIN claim_status cs ON cl.claim_status_id = cs.claim_status_id
            ORDER BY cl.claim_number
        """)
        with get_db() as db:
            rows = db.execute(sql).fetchall()
        reports = []
        for row in rows:
            reports.append(ClaimReport(
                client_name=f"{row[0]} {row[1]}", policy_number=row[2],
                insurance_type=row[3], claim_number=row[4], claim_type=row[5],
                incident_date=str(row[6]), claimed_amount=float(row[7]),
                claim_status=row[8], compensated_amount=float(row[9]) if row[9] else 0.0
            ))
        return reports

    def get_reinsurers_report(self) -> List[ReinsurerReport]:
        sql = text("""
            SELECT r.name, c.name, rt.description, it.description,
                   rp.participation_percentage
            FROM reinsurer r
            INNER JOIN country c ON r.country_id = c.country_id
            INNER JOIN reinsurance_type rt ON r.reinsurance_type_id = rt.reinsurance_type_id
            LEFT JOIN reinsurance_participation rp ON r.reinsurer_id = rp.reinsurer_id
            LEFT JOIN insurance_type it ON rp.insurance_type_id = it.insurance_type_id
            ORDER BY r.name, it.description
        """)
        with get_db() as db:
            rows = db.execute(sql).fetchall()
        reports = []
        for row in rows:
            reports.append(ReinsurerReport(
                reinsurer_name=row[0], country_name=row[1],
                reinsurance_type=row[2], insurance_type=row[3] or "",
                participation_percentage=float(row[4]) if row[4] else 0.0
            ))
        return reports

    def get_expired_policies_report(self) -> List[ExpiredPolicyReport]:
        sql = text("""
            SELECT p.policy_number, c.first_name, c.last_name, it.description,
                   p.start_date, p.end_date, p.insured_amount
            FROM policy p
            INNER JOIN client c ON p.client_id = c.client_id
            INNER JOIN insurance_type it ON p.insurance_type_id = it.insurance_type_id
            WHERE p.end_date < CURRENT_DATE
            ORDER BY p.end_date
        """)
        with get_db() as db:
            rows = db.execute(sql).fetchall()
        reports = []
        for row in rows:
            reports.append(ExpiredPolicyReport(
                policy_number=row[0], client_name=f"{row[1]} {row[2]}",
                insurance_type=row[3], start_date=str(row[4]),
                end_date=str(row[5]), insured_amount=float(row[6])
            ))
        return reports

    def get_cancelled_policies_report(self) -> List[CancelledPolicyReport]:
        sql = text("""
            SELECT c.first_name, c.last_name, c.identification_number,
                   COUNT(p.policy_number),
                   STRING_AGG(COALESCE(p.cancellation_reason, 'Not specified'), ', ')
            FROM client c
            INNER JOIN policy p ON c.client_id = p.client_id
            INNER JOIN policy_status ps ON p.policy_status_id = ps.policy_status_id
            WHERE ps.description = 'Cancelada'
            GROUP BY c.client_id, c.first_name, c.last_name, c.identification_number
            ORDER BY c.last_name, c.first_name
        """)
        with get_db() as db:
            rows = db.execute(sql).fetchall()
        reports = []
        for row in rows:
            reports.append(CancelledPolicyReport(
                client_name=f"{row[0]} {row[1]}",
                identification_number=row[2], cancelled_policies=row[3],
                cancellation_reasons=row[4]
            ))
        return reports

    def get_policy_summary_report(self) -> List[PolicySummaryReport]:
        sql = text("""
            SELECT it.description, COUNT(p.policy_number),
                   SUM(p.monthly_premium), SUM(p.insured_amount)
            FROM policy p
            INNER JOIN insurance_type it ON p.insurance_type_id = it.insurance_type_id
            INNER JOIN policy_status ps ON p.policy_status_id = ps.policy_status_id
            WHERE ps.description = 'Activa'
            GROUP BY it.description
            ORDER BY it.description
        """)
        with get_db() as db:
            rows = db.execute(sql).fetchall()
        reports = []
        for row in rows:
            reports.append(PolicySummaryReport(
                insurance_type=row[0], active_policies=row[1],
                total_monthly_premium=float(row[2]),
                total_insured_amount=float(row[3])
            ))
        return reports

    def get_claim_status_summary_report(self) -> List[ClaimStatusSummaryReport]:
        sql = text("""
            SELECT cs.description, COUNT(c.claim_number),
                   SUM(c.claimed_amount), SUM(COALESCE(c.compensated_amount, 0))
            FROM claim c
            INNER JOIN claim_status cs ON c.claim_status_id = cs.claim_status_id
            GROUP BY cs.description
            ORDER BY cs.description
        """)
        with get_db() as db:
            rows = db.execute(sql).fetchall()
        reports = []
        for row in rows:
            reports.append(ClaimStatusSummaryReport(
                claim_status=row[0], total_claims=row[1],
                total_claimed_amount=float(row[2]),
                total_compensated_amount=float(row[3])
            ))
        return reports

    def get_monthly_income_report(self) -> List[MonthlyIncomeReport]:
        sql = text("""
            SELECT EXTRACT(MONTH FROM p.start_date) AS month_number,
                   TO_CHAR(p.start_date, 'Month'),
                   SUM(p.monthly_premium)
            FROM policy p
            INNER JOIN policy_status ps ON p.policy_status_id = ps.policy_status_id
            WHERE ps.description = 'Activa'
            GROUP BY EXTRACT(MONTH FROM p.start_date), TO_CHAR(p.start_date, 'Month')
            ORDER BY month_number
        """)
        with get_db() as db:
            rows = db.execute(sql).fetchall()
        reports = []
        for row in rows:
            reports.append(MonthlyIncomeReport(
                month_name=row[1].strip(),
                monthly_income=float(row[2])
            ))
        return reports

    def get_approved_claims_report(self) -> List[ApprovedClaimsReport]:
        sql = text("""
            SELECT c.first_name, c.last_name, c.identification_number,
                   COUNT(cl.claim_number), SUM(cl.compensated_amount)
            FROM client c
            INNER JOIN policy p ON c.client_id = p.client_id
            INNER JOIN claim cl ON p.policy_number = cl.policy_number
            INNER JOIN claim_status cs ON cl.claim_status_id = cs.claim_status_id
            WHERE cs.description = 'Aprobado'
            GROUP BY c.client_id, c.first_name, c.last_name, c.identification_number
            ORDER BY c.last_name, c.first_name
        """)
        with get_db() as db:
            rows = db.execute(sql).fetchall()
        reports = []
        for row in rows:
            reports.append(ApprovedClaimsReport(
                client_name=f"{row[0]} {row[1]}",
                identification_number=row[2], approved_claims=row[3],
                total_compensated_amount=float(row[4]) if row[4] else 0.0
            ))
        return reports

    def get_rejected_claims_report(self) -> List[RejectedClaimsReport]:
        sql = text("""
            SELECT c.first_name, c.last_name, c.identification_number,
                   COUNT(cl.claim_number), cl.rejection_reason
            FROM client c
            INNER JOIN policy p ON c.client_id = p.client_id
            INNER JOIN claim cl ON p.policy_number = cl.policy_number
            INNER JOIN claim_status cs ON cl.claim_status_id = cs.claim_status_id
            WHERE cs.description = 'Rechazado'
            GROUP BY c.client_id, c.first_name, c.last_name, c.identification_number,
                     cl.rejection_reason
            ORDER BY c.last_name, c.first_name
        """)
        with get_db() as db:
            rows = db.execute(sql).fetchall()
        reports = []
        for row in rows:
            reports.append(RejectedClaimsReport(
                client_name=f"{row[0]} {row[1]}",
                identification_number=row[2], rejected_claims=row[3],
                rejection_reason=row[4] or ""
            ))
        return reports

    def get_client_details_report(self) -> List[dict]:
        sql = text("""
            SELECT c.client_id, c.first_name, c.last_name,
                   c.identification_number, c.age, c.address, c.phone, c.email,
                   g.description AS gender, co.name AS country, a.name AS agency,
                   (SELECT COUNT(*) FROM policy p2
                    INNER JOIN policy_status ps ON p2.policy_status_id = ps.policy_status_id
                    WHERE p2.client_id = c.client_id AND ps.description = 'Activa'),
                   (SELECT COALESCE(SUM(monthly_premium), 0) FROM policy p3
                    WHERE p3.client_id = c.client_id)
            FROM client c
            INNER JOIN gender g ON c.gender_id = g.gender_id
            INNER JOIN country co ON c.country_id = co.country_id
            INNER JOIN agency a ON c.agency_id = a.agency_id
            ORDER BY c.last_name, c.first_name
        """)
        with get_db() as db:
            rows = db.execute(sql).fetchall()
        return [
            dict(
                client_id=r[0], first_name=r[1], last_name=r[2],
                identification_number=r[3], age=r[4], address=r[5],
                phone=r[6], email=r[7], gender=r[8], country=r[9],
                agency=r[10], active_policies=r[11],
                total_premiums=float(r[12]),
            )
            for r in rows
        ]

    def get_agency_report(self) -> List[AgencyReport]:
        sql = text("SELECT name, address, phone, email, general_director, insurance_manager, claims_manager FROM agency")
        with get_db() as db:
            rows = db.execute(sql).fetchall()
        reports = []
        for row in rows:
            reports.append(AgencyReport(
                name=row[0], address=row[1], phone=row[2], email=row[3],
                general_director=row[4], insurance_manager=row[5], claims_manager=row[6]
            ))
        return reports

    def get_client_profile_report(self, client_id: int) -> List[ClientProfileReport]:
        sql = text("""
            SELECT c.first_name, c.last_name, c.identification_number,
                   c.phone, c.address, c.email,
                   (SELECT COUNT(*) FROM policy p2
                    INNER JOIN policy_status ps ON p2.policy_status_id = ps.policy_status_id
                    WHERE p2.client_id = c.client_id AND ps.description = 'Active'),
                   (SELECT COALESCE(SUM(monthly_premium), 0) FROM policy p3
                    WHERE p3.client_id = c.client_id),
                   cl.claim_number, cl.incident_date, cl.claimed_amount, cl.compensated_amount
            FROM client c
            LEFT JOIN policy p ON c.client_id = p.client_id
            LEFT JOIN claim cl ON p.policy_number = cl.policy_number
            WHERE c.client_id = :client_id
        """)
        with get_db() as db:
            rows = db.execute(sql, {"client_id": client_id}).fetchall()
        reports = []
        for row in rows:
            reports.append(ClientProfileReport(
                client_name=f"{row[0]} {row[1]}",
                identification_number=row[2], phone=row[3], address=row[4],
                email=row[5], active_policies=row[6], total_premiums_paid=float(row[7]),
                claim_number=row[8] or 0, incident_date=str(row[9]) if row[9] else "",
                claimed_amount=float(row[10]) if row[10] else 0.0,
                compensated_amount=float(row[11]) if row[11] else 0.0
            ))
        return reports
