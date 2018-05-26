# -*- coding: UTF-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Enum,DATE,Integer, String,ForeignKey, BIGINT
from sqlalchemy.orm import sessionmaker,relationship

engine = create_engine('mysql+mysqldb://man_user:674099@localhost:3306/snailblog')
Base = declarative_base()  # 生成orm基类

class Stu(Base):
    __tablename__ = "stu"
    id = Column(BIGINT, primary_key=True)
    name = Column(String(32),nullable=False)
    register_date = Column(DATE,nullable=False)
    def __repr__(self):
        return "<id:%s name:%s>" % (self.id, self.name)

class StudyRecord(Base):
    __tablename__ = "study_record"
    id = Column(Integer, primary_key=True)
    day = Column(Integer,nullable=False)
    status = Column(String(32),nullable=False)
    stu_id = Column(BIGINT,ForeignKey("stu.id"))  #------外键关联------
    #这个允许你在user表里通过backref字段反向查出所有它在stu2表里的关联项数据
    stu = relationship("Stu", backref="my_study_record")  # 添加关系，反查（在内存里）
    def __repr__(self):
        return "<name:%s day:%s status:%s>" % (self.stu.name, self.day,self.status)

Base.metadata.create_all(engine)  # 创建表结构
#Base.metadata.drop_all(engine)