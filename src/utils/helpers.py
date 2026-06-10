import re
from datetime import date, datetime


def validate_email(email: str) -> bool:
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    return bool(re.match(r"^\+?[\d\s\-()]{7,20}$", phone))


def parse_date(value: str) -> date:
    return datetime.strptime(value, "%Y-%m-%d").date()


def format_date(d: date) -> str:
    return d.isoformat() if d else ""
