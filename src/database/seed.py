from datetime import date, timedelta
from src.database.connection import engine, Base
from src.models import *
from src.services.claim_status_service import ClaimStatusService
from src.services.claim_type_service import ClaimTypeService
from src.services.country_service import CountryService
from src.services.gender_service import GenderService
from src.services.insurance_type_service import InsuranceTypeService
from src.services.policy_status_service import PolicyStatusService
from src.services.reinsurance_type_service import ReinsuranceTypeService
from src.services.role_service import RoleService
from src.services.agency_service import AgencyService
from src.services.client_service import ClientService
from src.services.policy_service import PolicyService
from src.services.coverage_service import CoverageService
from src.services.claim_service import ClaimService
from src.services.reinsurer_service import ReinsurerService
from src.services.reinsurance_participation_service import ReinsuranceParticipationService
from src.services.user_service import UserService


def seed_all():
    svc_cs = ClaimStatusService()
    if svc_cs.get_all():
        print("Seed data already exists, skipping.")
        return

    print("Seeding lookup tables...")
    svc_cs.create(description="Pendiente")
    svc_cs.create(description="En Proceso")
    svc_cs.create(description="Aprobado")
    svc_cs.create(description="Rechazado")
    print("  ClaimStatus done.")

    svc_ct = ClaimTypeService()
    svc_ct.create(description="Accidente")
    svc_ct.create(description="Robo")
    svc_ct.create(description="Incendio")
    svc_ct.create(description="Desastre Natural")
    svc_ct.create(description="Salud")
    print("  ClaimType done.")

    svc_co = CountryService()
    countries = [
        ("Cuba", "CU"), ("Estados Unidos", "US"), ("España", "ES"),
        ("México", "MX"), ("Argentina", "AR"), ("Colombia", "CO"),
        ("Brasil", "BR"), ("Chile", "CL"), ("Perú", "PE"),
        ("Venezuela", "VE"), ("Canadá", "CA"), ("Alemania", "DE"),
        ("Francia", "FR"), ("Italia", "IT"), ("Reino Unido", "GB"),
        ("Rusia", "RU"), ("China", "CN"), ("Japón", "JP"),
        ("India", "IN"), ("Australia", "AU"),
    ]
    for name, code in countries:
        svc_co.create(name=name, iso_code=code)
    print("  Country done.")

    svc_g = GenderService()
    svc_g.create(description="Masculino")
    svc_g.create(description="Femenino")
    print("  Gender done.")

    svc_it = InsuranceTypeService()
    svc_it.create(description="Vida")
    svc_it.create(description="Automóvil")
    svc_it.create(description="Hogar")
    svc_it.create(description="Salud")
    svc_it.create(description="Viaje")
    print("  InsuranceType done.")

    svc_ps = PolicyStatusService()
    svc_ps.create(description="Activa")
    svc_ps.create(description="Cancelada")
    svc_ps.create(description="Expirada")
    print("  PolicyStatus done.")

    svc_rt = ReinsuranceTypeService()
    svc_rt.create(description="Proporcional")
    svc_rt.create(description="No Proporcional")
    svc_rt.create(description="Facultativo")
    print("  ReinsuranceType done.")

    svc_rl = RoleService()
    svc_rl.create(name="admin")
    print("  Role done.")

    print("Creating Agency...")
    svc_a = AgencyService()
    agency = svc_a.create(
        name="Aseguradora Nacional S.A.",
        address="Calle 123, Vedado, La Habana",
        phone="+53 7 123 4567",
        email="contacto@aseguradoranacional.cu",
        general_director="Dr. Juan Pérez",
        insurance_manager="Lic. María García",
        claims_manager="Ing. Carlos López",
    )
    print(f"  Agency id={agency.agency_id}")

    print("Creating Clients...")
    svc_cl = ClientService()
    clients_data = [
        ("Ana", "Martínez Rodríguez", "001-123456-78", 30, "Calle A #123, Centro Habana", "+53 5 111 2233", "ana@email.com", 2, 1),
        ("Pedro", "González Díaz", "001-234567-89", 45, "Av. B #456, Miramar", "+53 5 222 3344", "pedro@email.com", 1, 1),
        ("María", "López Hernández", "001-345678-90", 28, "Calle C #789, Playa", "+53 5 333 4455", "maria@email.com", 2, 1),
        ("José", "Ramírez Torres", "001-456789-01", 55, "Calle D #321, Cerro", "+53 5 444 5566", "jose@email.com", 1, 1),
        ("Laura", "Fernández García", "001-567890-12", 35, "Av. E #654, Nuevo Vedado", "+53 5 555 6677", "laura@email.com", 2, 1),
    ]
    clients = []
    for fn, ln, idnum, age, addr, phone, email, gid, coid in clients_data:
        c = svc_cl.create(
            agency_id=agency.agency_id,
            gender_id=gid,
            country_id=coid,
            first_name=fn,
            last_name=ln,
            identification_number=idnum,
            age=age,
            address=addr,
            phone=phone,
            email=email,
        )
        clients.append(c)
    print(f"  {len(clients)} clients created.")

    print("Creating Reinsurers...")
    svc_r = ReinsurerService()
    reinsurers_data = [
        ("Reaseguradora Internacional S.A.", 1, 2),
        ("Seguros Globales Ltd.", 2, 5),
        ("Protección Mundial Corp.", 3, 1),
    ]
    reinsurers = []
    for name, rtid, coid in reinsurers_data:
        r = svc_r.create(
            agency_id=agency.agency_id,
            reinsurance_type_id=rtid,
            country_id=coid,
            name=name,
        )
        reinsurers.append(r)
    print(f"  {len(reinsurers)} reinsurers created.")

    print("Creating Reinsurance Participations...")
    svc_rp = ReinsuranceParticipationService()
    participations = [
        (reinsurers[0].reinsurer_id, 1, 30.00),
        (reinsurers[0].reinsurer_id, 2, 25.00),
        (reinsurers[1].reinsurer_id, 3, 40.00),
        (reinsurers[2].reinsurer_id, 4, 20.00),
        (reinsurers[2].reinsurer_id, 5, 35.00),
    ]
    for rid, itid, pct in participations:
        svc_rp.create(
            reinsurer_id=rid,
            insurance_type_id=itid,
            participation_percentage=pct,
        )
    print(f"  {len(participations)} participations created.")

    print("Creating Policies...")
    svc_p = PolicyService()
    today = date.today()
    policies_data = [
        # (client_id, insurance_type_id, policy_status_id, start_date, end_date, monthly_premium, insured_amount, cancellation_reason)
        # --- Activas ---
        (clients[0].client_id, 2, 1, today - timedelta(days=365), today + timedelta(days=30),  150.00, 25000.00, None),
        (clients[1].client_id, 1, 1, today - timedelta(days=180), today + timedelta(days=185),  80.00, 100000.00, None),
        (clients[2].client_id, 3, 1, today - timedelta(days=90),  today + timedelta(days=275), 200.00, 50000.00, None),
        (clients[3].client_id, 4, 1, today - timedelta(days=60),  today + timedelta(days=305), 120.00, 30000.00, None),
        (clients[4].client_id, 5, 1, today - timedelta(days=30),  today + timedelta(days=335),  60.00, 15000.00, None),
        # --- Expiradas (end_date anterior a hoy, status Expirada) ---
        (clients[1].client_id, 4, 3, today - timedelta(days=700), today - timedelta(days=200),  90.00, 80000.00, None),
        (clients[4].client_id, 2, 3, today - timedelta(days=600), today - timedelta(days=150),  65.00, 18000.00, None),
        (clients[0].client_id, 5, 3, today - timedelta(days=450), today - timedelta(days=10),   45.00, 10000.00, None),
        (clients[3].client_id, 1, 3, today - timedelta(days=800), today - timedelta(days=300), 110.00, 60000.00, None),
        # --- Canceladas (status Cancelada, con motivo) ---
        (clients[0].client_id, 1, 2, today - timedelta(days=500), today - timedelta(days=135), 100.00, 50000.00, "Cliente solicitó cancelación"),
        (clients[2].client_id, 3, 2, today - timedelta(days=400), today - timedelta(days=70),  180.00, 40000.00, "Impago de prima"),
        (clients[3].client_id, 4, 2, today - timedelta(days=350), today - timedelta(days=20),  110.00, 25000.00, "Incumplimiento de condiciones"),
        (clients[2].client_id, 2, 2, today - timedelta(days=550), today - timedelta(days=200), 130.00, 35000.00, "Riesgo no asegurable detectado"),
    ]
    policies = []
    for cid, itid, psid, sd, ed, mp, ia, cr in policies_data:
        kwargs = dict(
            client_id=cid, insurance_type_id=itid, policy_status_id=psid,
            start_date=sd, end_date=ed, monthly_premium=mp, insured_amount=ia,
        )
        if cr is not None:
            kwargs["cancellation_reason"] = cr
        p = svc_p.create(**kwargs)
        policies.append(p)
    activas = sum(1 for p in policies_data if p[2] == 1)
    expiradas = sum(1 for p in policies_data if p[2] == 3)
    canceladas = sum(1 for p in policies_data if p[2] == 2)
    print(f"  {len(policies)} policies created ({activas} activas, {expiradas} expiradas, {canceladas} canceladas).")

    print("Creating Coverages...")
    svc_cov = CoverageService()
    coverages_data = [
        (policies[0].policy_number, "Cobertura total contra accidentes", 25000.00),
        (policies[0].policy_number, "Responsabilidad civil", 10000.00),
        (policies[1].policy_number, "Cobertura de vida completa", 100000.00),
        (policies[2].policy_number, "Cobertura contra incendio", 50000.00),
        (policies[3].policy_number, "Cobertura médica hospitalaria", 30000.00),
        (policies[4].policy_number, "Cobertura de viaje internacional", 15000.00),
    ]
    for pn, desc, amount in coverages_data:
        svc_cov.create(
            policy_number=pn,
            description=desc,
            coverage_amount=amount,
        )
    print(f"  {len(coverages_data)} coverages created.")

    print("Creating Claims...")
    svc_clm = ClaimService()
    claims_data = [
        (policies[0].policy_number, 1, 2, today - timedelta(days=30), 5000.00, 3500.00, None),
        (policies[0].policy_number, 2, 1, today - timedelta(days=15), 12000.00, None, None),
        (policies[2].policy_number, 3, 3, today - timedelta(days=45), 30000.00, 25000.00, None),
        (policies[3].policy_number, 5, 4, today - timedelta(days=60), 8000.00, None, "Preexistencia no cubierta"),
    ]
    for pn, ctid, csid, idate, ca, comp, rr in claims_data:
        kwargs = dict(
            policy_number=pn,
            claim_type_id=ctid,
            claim_status_id=csid,
            incident_date=idate,
            claimed_amount=ca,
        )
        if comp is not None:
            kwargs["compensated_amount"] = comp
        if rr is not None:
            kwargs["rejection_reason"] = rr
        svc_clm.create(**kwargs)
    print(f"  {len(claims_data)} claims created.")

    print("Creating additional Users...")
    svc_u = UserService()
    if not svc_u.get_by_id(1):
        svc_u.create(
            role_id=1,
            username="admin",
            password="admin",
            full_name="System Administrator",
            active=True,
        )
    if not svc_u.get_by_id(2):
        svc_u.create(
            role_id=1,
            username="operador",
            password="operador",
            full_name="Operador del Sistema",
            active=True,
        )
    if not svc_u.get_by_id(3):
        svc_u.create(
            role_id=1,
            username="consultor",
            password="consultor",
            full_name="Consultor de Seguros",
            active=True,
        )
    print("  Users created.")

    print("\nSeed data completed successfully!")


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    seed_all()
