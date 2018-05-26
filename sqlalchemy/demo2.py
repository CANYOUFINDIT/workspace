# -*- coding: UTF-8 -*-
# 导入:
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类,生成orm基类:
Base = declarative_base()

# 初始化数据库连接,创建实例，连接snailblog库,echo=True 显示信息
engine = create_engine('mysql+mysqldb://man_user:674099@localhost:3306/snailblog', encoding='utf-8')

# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'user'

    # 表的结构:
    id = Column(Integer, nullable = False, primary_key = True)
    name = Column(String(20), nullable = False)
    # 一对多:
    books = relationship('Book')

# 定义Book对象:
class Book(Base):
    __tablename__ = 'book'

    id = Column(String(20), primary_key=True)
    name = Column(String(20))
    # “多”的一方的book表是通过外键关联到user表的:
    #允许你在user表里通过backref字段反向查出所有它在stu2表里的关联项数据
    user_id = Column(Integer, ForeignKey("stu2.id"))

#建立所有表
def init_db():
    #创建表结构 （这里是父类调子类）
    Base.metadata.create_all(engine)

#删除所有表
def drop_db():
    Base.metadata.drop_all(engine)

# 创建session对象:
session = DBSession()
# 创建新User对象:
#new_user = User(id='5', name='Bob')
# 添加到session:
#session.add(new_user)
# 提交即保存到数据库:
#session.commit()

# 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
user = session.query(User).filter(User.id=='5').one()
# 打印类型和对象的name属性:
print 'type:', type(user)
print 'name:', user.name

# 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
user = session.query(User).all()
# 打印类型和对象的name属性:
print "-------all-------"
print 'type:', type(user)
print 'user:', user[0]
print 'name:', user[0].name
# 关闭Session:
session.close()