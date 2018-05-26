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

Session_class = sessionmaker(bind=engine)  # 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
session = Session_class()  # 生成session实例 #cursor

s1 = Stu(name="A",register_date="2014-05-21")
s2 = Stu(name="J",register_date="2014-03-21")
s3 = Stu(name="R",register_date="2014-02-21")
s4 = Stu(name="E",register_date="2013-01-21")

study_obj1 = StudyRecord(day=1,status="YES", stu_id=1)
study_obj2 = StudyRecord(day=2,status="NO", stu_id=1)
study_obj3 = StudyRecord(day=3,status="YES", stu_id=1)
study_obj4 = StudyRecord(day=1,status="YES", stu_id=2)

session.add_all([s1,s2,s3,s4,study_obj1,study_obj2,study_obj3,study_obj4])  # 创建

#Base.metadata.drop_all(engine) 
session.commit()

stu_obj = session.query(Stu).filter(Stu.name=="A").first()  # 查询
print stu_obj
# 在stu2表，查到StudyRecord表的记录
print(stu_obj.my_study_record)  # 查询A一共上了几节课

session.close()