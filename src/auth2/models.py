from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(30), unique=True, index=True)
    password = Column(String(150))

    # videos = relationship('Video', back_populates='creator')


    # for video databse
    # creator = relationship('User', back_populates='videos')