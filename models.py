from typing import Text
from .database import Base
from sqlalchemy import Column, Integer, String,ForeignKey,Text,DateTime



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)

class Summary(Base):
    __tablename__ = 'summaries'
    
    id = Column(Integer,primary_key=True,index=True)
    original_text = Column(Text, nullable=False)
    summary_text = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

class Upload(Base):
    __tablename__ = 'uploads'
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    text = Column(Text, nullable=False)

class Note(Base):
    __tablename__='notes'
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    notes=Column(Text,nullable=False)


class Quiz(Base):
    __tablename__='quizes'
    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quizes=Column(Text,nullable=False)