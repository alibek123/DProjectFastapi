from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2 as pg
from psycopg2.extras import RealDictCursor

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:123@localhost/diplomdb'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()


# try:
#     conn = pg.connect(host='localhost', database='diplomdb', user='postgres', password='123',
#                       cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
# except Exception as e:
#     print(e)
#
