import psycopg2
import time

from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# #Psycopg Module if needed
# while True:
#     try:
#         db_connection = psycopg2.connect(host='localhost', database='FastApiApp', user='postgres', password='postgres',
#                                         cursor_factory=RealDictCursor)
#         cursor = db_connection.cursor()
#         print("Database connection was successful.")
#         break
#     except Exception as error:
#         print(f"Connection to database failed.")
#         print("Error: ", error)
#         time.sleep(2)
