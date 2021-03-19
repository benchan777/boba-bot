from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

association_table = Table('association', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('boba_store_id', Integer, ForeignKey('boba_store.id'))
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer)
    username = Column(String(200))
    location = Column(String(200))
    server_id = Column(String(200))
    server_name = Column(String(200))
    user_order_info = Column(String(200))
    user_order = relationship(
        'BobaShop',
        secondary = association_table,
        back_populates = 'user_with_order'
    )

class BobaShop(Base):
    __tablename__ = 'boba_store'

    id = Column(Integer, primary_key = True)
    store_id = Column(String(200))
    name = Column(String(200))
    city = Column(String(200))
    user_with_order = relationship(
        'User',
        secondary = association_table,
        back_populates = 'user_order'
    )