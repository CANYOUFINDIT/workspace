# -*- coding: UTF-8 -*-
# 导入:
from sqlalchemy import Column, String, Integer, BIGINT, create_engine, CHAR, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

class User(Base):
    __tablename__='user'
    id = Column(BIGINT,primary_key = True, autoincrement=True)
    name = Column(CHAR(20))
    sex = Column(CHAR(1))
    birthday = Column(Integer)
    collage = Column(CHAR(20))
    major = Column(CHAR(20))
    grade =  Column(Integer)
    password =  Column(CHAR(20))
    power = Column(Integer)

class Class(Base):
    __tablename__='class'
    id = Column(Integer,primary_key = True, autoincrement=True) #设置主键
    cname = Column(CHAR(20))

class Grade(Base):
    __tablename__ = 'grade'
    id = Column(Integer,primary_key=True, autoincrement=True)
    score = Column(Integer)

def init_db():
    Base.metadata.create_all(engine)

def drop_db():
    Base.metadata.drop_all(engine)

# 初始化数据库连接:
engine = create_engine('mysql+mysqldb://man_user:674099@localhost:3306/snailblog')
# 创建Session类型:
Session = sessionmaker(bind=engine)

#init_db()
drop_db()
