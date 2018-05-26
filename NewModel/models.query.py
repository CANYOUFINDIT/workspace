# -*- coding: UTF-8 -*-
import models
from sqlalchemy.orm import sessionmaker

Session_class = sessionmaker(bind=models.engine)
session = Session_class()

sub1 = session.query(models.Subject).filter(models.Subject.id == 1).first()
stu1 = session.query(models.Student).filter(models.Student.id == 1).first()
tea1 = session.query(models.Teacher).filter(models.Teacher.id == 1).first()
cla1 = session.query(models.Classes).filter(models.Classes.id == 1).first()
col1 = session.query(models.Collage).filter(models.Collage.id == 1).first()

#查询课程下的学生
print sub1.student
#查询学生的课程
print stu1.subject
#查询学生的老师
print stu1.teacher
#查询老师的学生
print tea1.student
#查询学生的班级
print stu1.cla
#查询班级里的学生
print cla1.student
#查询老师所属的学院
print tea1.collages
#查询学院里的老师
print col1.teacher
#查询班级所属的学院
print cla1.collages
#查询学院下的班级
print col1.classes
