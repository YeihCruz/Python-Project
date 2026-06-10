from src.database.connection import engine, Base
from src.models import *

Base.metadata.drop_all(bind=engine)
print("All tables dropped.")
