# connecting to db using sqlalchemy

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLACHEMY_DATABSE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLACHEMY_DATABSE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()









# connecting to db using raw sql
# import time
# import psycopg2
# from psycopg2.extras import RealDictCursor

# while True:

#     try:
#         conn = psycopg2.connect(host='..', database='..', user='..', password='..', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("DB Connection successful!")
#         break
#     except Exception as error:
#         print("DB Connection failed!") 
#         print("Error: ", error)
#         time.sleep(2)
