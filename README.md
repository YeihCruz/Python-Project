# InsuranceAgency - Python (SQLAlchemy + tkinter)

Migración del proyecto Java de escritorio (Insurance Agency Management System) a Python.

## Arquitectura

- **ORM**: SQLAlchemy 2.x (DeclarativeBase)
- **UI**: tkinter (estándar)
- **BD**: PostgreSQL
- **Migraciones**: Alembic

## Estructura

```
src/
├── config/        # Configuración (variables de entorno)
├── database/      # Conexión y sesión de BD
├── models/        # Modelos SQLAlchemy (1 por entidad)
├── repositories/  # Capa de acceso a datos (CRUD)
├── services/      # Lógica de negocio
├── ui/            # Interfaz gráfica (tkinter)
└── utils/         # Validaciones y helpers
```

## Instalación

```bash
pip install -r requirements.txt
cp .env.example .env
# Editar .env con credenciales de BD
python -m src.main
```

## Base de datos

El proyecto espera una base PostgreSQL con el esquema definido en `SQL.sql`
del proyecto Java original. Ejecutar migraciones:

```bash
alembic upgrade head
```

## Entidades

- Agency, Client, Policy, Claim, Coverage, Reinsurer
- ReinsuranceParticipation, Country, Gender, InsuranceType
- PolicyStatus, ClaimType, ClaimStatus, ReinsuranceType
- Role, User
