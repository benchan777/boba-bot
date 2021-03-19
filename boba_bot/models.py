from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer)
    username = Column(String(200))
    location = Column(String(200))
    server_id = Column(String(200))
    server_name = Column(String(200))