from sqlalchemy import Integer, String, Column
from database import Base


class User(Base):
    __tablename__ = "User"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(30), unique=True, index=True)
    password = Column(String(150))