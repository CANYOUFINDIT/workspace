# -*- coding: UTF-8 -*-
from sqlalchemy import create_engine
from sqlalchemy import Table, MetaData, Column, Integer, String
from sqlalchemy.orm import mapper, sessionmaker
# 创建实例，并连接test库
engine = create_engine('mysql+mysqldb://man_user:674099@localhost:3306/snailblog')

metadata = MetaData()

user = Table('user', metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String(50)),
            Column('password', String(12))
        )

class User(object):
    def __init__(self, name, id, password):
        self.id = id
        self.name = name
        self.password = password
    #控制打印
    def __repr__(self):
        return "<User(id = '%s', name = '%s', password = '%s')>" % (self.id, self.name, self.password)

# 类User 和 user关联起来
mapper(User, user)
# 如果数据库里有，就不会创建了。
metadata.create_all(engine)
# 创建与数据库的会话session,注意,这里返回给session的是个class,不是实例
DBSession = sessionmaker(bind=engine)  # 实例和engine绑定
session = DBSession()  # 生成session实例，相当于游标

#new_user = User(id=2,name='b',password='123456')  # 生成你要创建的数据对象
#session.add(new_user)  # 把要创建的数据对象添加到这个session里， 一会统一创建
#print (new_user.name,new_user.id) #此时也依然还没创建
#session.commit() #现此才统一提交，创建数据

my_user = session.query(User).filter_by(name="b").filter_by(id = '2').first()  # 查询，把数据返回成对象，filter方法判断相等使用'=='
print(my_user.id, my_user.name, my_user.password) #通过调用对象属性，打印查询结果
print my_user      #__repr__响应控制打印

my_user.name = "b"  # 查询出来之后直接赋值修改
my_user.id = 2
my_user.password = "123456"
session.commit()
#打印user表所有行
print(session.query(User).all() )

session.close()