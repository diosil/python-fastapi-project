from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

POSTGRES_USERNAME = settings.database_username
POSTGRES_PASSWORD = settings.database_password
POSTGRES_ADDRESS = settings.database_hostname+":"+settings.database_port
POSTGRES_DATABASE = settings.database_name

SQLALCHEMY_DATABASE_URL = f'postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_ADDRESS}/{POSTGRES_DATABASE}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
---- First try using psycopg2 connection
---- Was replaced by SQLAlchemy connection

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='admin', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connected successfully!')
        break
    except Exception as Error:
        print('Connection to database failed')
        print('Error: ', Error)
        time.sleep(2)
"""