from config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

class DBBase(DeclarativeBase):
    pass

DATABASE_URL = Config().DATABASE_URL
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL is not set in the configuration.")

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    DBBase.metadata.create_all(engine)