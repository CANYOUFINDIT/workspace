# -*- coding: UTF-8 -*-
import more_tables
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Enum,DATE,Integer, String,ForeignKey, BIGINT
from sqlalchemy.orm import sessionmaker,relationship

Session_class = sessionmaker(bind=more_tables.engine)  # 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
session = Session_class()  # 生成session实例 #cursor

s1 = more_tables.Stu(name="A",register_date="2014-05-21")
s2 = more_tables.Stu(name="J",register_date="2014-03-21")
s3 = more_tables.Stu(name="R",register_date="2014-02-21")
s4 = more_tables.Stu(name="E",register_date="2013-01-21")

study_obj1 = more_tables.StudyRecord(day=1,status="YES", stu_id=1)
study_obj2 = more_tables.StudyRecord(day=2,status="NO", stu_id=1)
study_obj3 = more_tables.StudyRecord(day=3,status="YES", stu_id=1)
study_obj4 = more_tables.StudyRecord(day=1,status="YES", stu_id=2)

session.add_all([s1,s2,s3,s4,study_obj1,study_obj2,study_obj3,study_obj4])  # 创建

#Base.metadata.drop_all(engine) 
session.commit()

stu_obj = session.query(more_tables.Stu).filter(more_tables.Stu.name=="A").first()  # 查询
print stu_obj
# 在stu2表，查到StudyRecord表的记录
print(stu_obj.my_study_record)  # 查询A一共上了几节课

session.close()