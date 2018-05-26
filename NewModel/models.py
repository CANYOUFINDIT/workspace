# -*- coding: UTF-8 -*-
from sqlalchemy import Table, Column, Integer,String,DATE, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

db_user = 'man_user'
passwd = '674099'
database = 'snailblog'

eng = "mysql+mysqldb://" + db_user + ":" + passwd + "@localhost:3306/" + database
engine = create_engine(eng, encoding='utf-8')

#学生与课程的多对多关系表
stu_to_sub = Table('stu_to_sub', Base.metadata,
                        Column('student_id',Integer,ForeignKey('student.id')),
                        Column('subject_id',Integer,ForeignKey('subject.id')),
                        )

#学生与老师的多对多关系表
stu_to_tea = Table('stu_to_tea', Base.metadata,
                        Column('student_id',Integer,ForeignKey('student.id')),
                        Column('teacher_id',Integer,ForeignKey('teacher.id')),
                        )


#学生表
class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer,primary_key=True)                                               #学号
    name = Column(String(10), nullable=False)                                           #姓名
    classes = Column(Integer, ForeignKey("classes.id"))                                 #班级
    password = Column(String(20), nullable=False)                                       #密码
    #建立与课程表的虚拟关系，实现查课程下的学生
    subject = relationship('Subject', secondary = stu_to_sub, backref = 'student')
    #建立与老师表的虚拟关系，实现查老师下的学生
    teacher = relationship('Teacher', secondary=stu_to_tea, backref='student')
    #建立与班级的虚拟关系，实现查班级下的学生
    cla = relationship('Classes', backref='student')

    def __repr__(self):
        return "<学生学号:%s 学生姓名:%s>" % (self.id, self.name)

#老师表
class Teacher(Base):
    __tablename__ = 'teacher'
    id = Column(Integer,primary_key=True)
    name = Column(String(10), nullable=False)                                           #姓名
    password = Column(String(20), nullable=False)   #密码
    #建立与学院的关系
    collage = Column(Integer, ForeignKey("collage.id"))
    #建立与学院的虚拟关系，实现查学院下的老师
    collages = relationship('Collage', backref='teacher')

    def __repr__(self):
        return "<老师id:%s 老师姓名:%s>" % (self.id, self.name)

#班级表
class Classes(Base):
    __tablename__ = 'classes'
    id = Column(Integer,primary_key=True)           #班级
    class_id = Column(Integer, nullable=False)
    collage = Column(Integer, ForeignKey("collage.id"))
    #建立与学院的虚拟关系，实现查学院下的班级
    collages = relationship('Collage', backref='classes')

    def __repr__(self):
        return "<班级id:%s 所属学院id:%s>" % (self.class_id, self.collage)

#课程表
class Subject(Base):
    __tablename__ = 'subject'
    id = Column(Integer,primary_key=True)
    name = Column(String(20), nullable=False)       #课程名
    #与老师关联，表明代课老师
    teacher = Column(Integer, ForeignKey("teacher.id"))
    teachers = relationship('Teacher', backref='subject')

    def __repr__(self):
        return "<课程名：%s 代课老师:%s >" % (self.name, self.teachers)

#成绩表
class Score(Base):
    __tablename__ = 'score'
    id = Column(Integer,primary_key=True)
    fraction = Column(Integer, nullable=False) #分数
    #外键关联
    student_id = Column(Integer, ForeignKey("student.id"))
    subject_id = Column(Integer, ForeignKey("subject.id"))
    #建立与课程的虚拟关系，实现查课程下的成绩
    subject = relationship('Subject', backref='score')
    #建立与学生的虚拟关系，实现查学生下的成绩
    student = relationship('Student', backref = 'score')

    def __repr__(self):
        return "<学生学号:%s 课程代号:%s 分数:%s>" % (self.student_id, self.subject_id, self.fraction) 

#学院表
class Collage(Base):
    __tablename__ = 'collage'
    id = Column(Integer,primary_key=True)           
    name = Column(String(10), nullable=False)       #学院名称

    def __repr__(self):
        return "<学院名称：%s>" % (self.name)

def init_db():
    Base.metadata.create_all(engine)

def drop_db():
    Base.metadata.drop_all(engine)

init_db()