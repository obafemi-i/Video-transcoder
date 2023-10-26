from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values

config = dotenv_values()


DATABASE_URL = config['DATABASE_URL']
# print(DATABASE_URL)
DATABASE_URL = "mysql+mysqlconnector://root@localhost:3306/auth"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

