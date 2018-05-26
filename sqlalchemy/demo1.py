# -*- coding: UTF-8 -*-
# 导入:
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 初始化数据库连接:
engine = create_engine('mysql+mysqldb://man_user:674099@localhost:3306/snailblog')

# 创建对象的基类:
Base = declarative_base()

# 创建DBSession类型:
# 创建与数据库的会话DBSession,注意,这里返回的是个class,不是实例,实例和engine绑定
DBSession = sessionmaker(bind=engine)

# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'user'

    # 表的结构:
    id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String(20), nullable=False)
    # 一对多:
    #books = relationship('Book')

class Book(Base):
    __tablename__ = 'book'

    id = Column(String(20), primary_key=True)
    name = Column(String(20))
    # “多”的一方的book表是通过外键关联到user表的:
    #user_id = Column(String(20), ForeignKey('user.id'))

#建立所有表
def init_db():
    Base.metadata.create_all(engine)

#删除所有表
def drop_db():
    Base.metadata.drop_all(engine)

#向表插入成员，参数(table_name, id, name)
def insert_user(table_name, get_id, get_name):
    # 创建session对象，相当于游标:
    session = DBSession()
    # 创建新User对象:
    new_user = table_name(id = get_id, name = get_name)
    # 添加到session:
    session.add(new_user)
    # 提交即保存到数据库:
    session.commit()
    # 关闭Session:
    session.close()

#查询操作，参数(表类名，查询条件，控制条件)
def search_user(table_class, key, get_id):
    session = DBSession()
    # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
    #sqlalchemy把返回的数据映射成一个对象啦，这样你调用每个字段就可以跟调用对象属性一样啦
    user = session.query(table_class).filter(key == get_id).one()
    # 打印类型和对象的name属性:
    print 'type:', type(user)
    print 'name:', user.name
    print 'id:', user.id
    # 关闭Session:
    session.close()
    
#init_db()
#insert_user(User, 11, 'Hell')
search_user(User, User.id, 11)