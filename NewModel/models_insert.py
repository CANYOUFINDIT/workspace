# -*- coding: UTF-8 -*-
import models
from sqlalchemy.orm import sessionmaker

Session_class = sessionmaker(bind=models.engine)
session = Session_class()

#插入学院
col1 = models.Collage(name = 'jky')
col2 = models.Collage(name = 'sky')
col3 = models.Collage(name = 'ty')
session.add_all([col1, col2, col3])
#插入班级
cla1 = models.Classes(class_id = 1604, collage = 1)
cla2 = models.Classes(class_id = 1605, collage = 1)
cla3 = models.Classes(class_id = 1607, collage = 1)
cla4 = models.Classes(class_id = 1604, collage = 2)
cla5 = models.Classes(class_id = 1605, collage = 2)
cla6 = models.Classes(class_id = 1607, collage = 3)
session.add_all([cla1,cla2,cla3,cla4,cla5,cla6])
#插入课程
sub1 = models.Subject(name = 'math', teacher = 1)
sub2 = models.Subject(name = 'English', teacher = 1)
sub3 = models.Subject(name = 'Chinese', teacher = 1)
session.add_all([sub1,sub2,sub3])
#插入学生
stu1 = models.Student(name = 'fty1', classes = 1, password = 'fty')
stu4 = models.Student(name = 'fty2', classes = 1, password = 'fty2')
stu2 = models.Student(name = 'xjh', classes = 2, password = 'xjh')
stu3 = models.Student(name = 'cw', classes = 3, password = 'cw')
stu5 = models.Student(name = 'lh', classes = 4, password = 'lh')
session.add_all([stu1,stu2,stu3,stu4,stu5])
#插入老师
tea1 = models.Teacher(name = 'a', collage = 1, password = 'a')
tea2 = models.Teacher(name = 'b', collage = 1, password = 'b')
tea3 = models.Teacher(name = 'c', collage = 1, password = 'c')
tea4 = models.Teacher(name = 'd', collage = 2, password = 'd')
tea5 = models.Teacher(name = 'e', collage = 2, password = 'e')
tea6 = models.Teacher(name = 'f', collage = 3, password = 'f')
session.add_all([tea1,tea2,tea3,tea4, tea5,tea6])
session.commit()

#建立学生与课程，老师的联系
cla1 = session.query(models.Subject).filter(models.Subject.id == 1).first()
cla2 = session.query(models.Subject).filter(models.Subject.id == 2).first()
cla3 = session.query(models.Subject).filter(models.Subject.id == 3).first()

stu1 = session.query(models.Student).filter(models.Student.id == 1).first()
stu2 = session.query(models.Student).filter(models.Student.id == 2).first()
stu3 = session.query(models.Student).filter(models.Student.id == 3).first()
stu4 = session.query(models.Student).filter(models.Student.id == 4).first()
stu5 = session.query(models.Student).filter(models.Student.id == 5).first()

tea1 = session.query(models.Teacher).filter(models.Teacher.id == 1).first()
tea2 = session.query(models.Teacher).filter(models.Teacher.id == 2).first()
tea3 = session.query(models.Teacher).filter(models.Teacher.id == 3).first()
tea4 = session.query(models.Teacher).filter(models.Teacher.id == 4).first()
tea5 = session.query(models.Teacher).filter(models.Teacher.id == 5).first()
tea6 = session.query(models.Teacher).filter(models.Teacher.id == 6).first()

stu1.subject = [cla1, cla2, cla3]
stu2.subject = [cla1, cla2, cla3]
stu3.subject = [cla1, cla2]
stu4.subject = [cla1, cla2, cla3]
stu5.subject = [cla2, cla3]

stu1.teacher = [tea1,tea2,tea3,tea4,tea5,tea6]
stu2.teacher = [tea2,tea3,tea4,tea5,tea6]
stu3.teacher = [tea3,tea4,tea5,tea6]
stu4.teacher = [tea4,tea5,tea6]
stu5.teacher = [tea5,tea6]

session.commit()
