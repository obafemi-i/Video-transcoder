from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values
import pymysql
config = dotenv_values()
# pymysql

DATABASE_URL = 'mysql+mysqlconnector://root@localhost:3306/auth'
# DATABASE_URL = 'mysql+pymsql://root@localhost:3306/auth'
# DATABASE_URL = config['DATABASE_URL']
# DATABASE_URL = 'mysql+pymsql://auth_user@host.minikube.internal:3306/auth'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

