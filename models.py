from sqlalchemy import Boolean, Column, Integer, String, Float
from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    content = Column(String(100))
    user_id = Column(Integer)

class Beer(Base):
    __tablename__ = 'beers'
    id = Column(Integer, primary_key=True, index=True)
    style = Column(String(50))
    alcohol = Column(Float)
    cereal = Column(String(100))