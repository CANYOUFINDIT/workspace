# -*- coding: UTF-8 -*-
# 添加数据
import foreignkey
from sqlalchemy.orm import sessionmaker

Session_class = sessionmaker(bind=foreignkey.engine)  # 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
session = Session_class()  # 生成session实例 #cursor
# 创建书
'''
b1 = foreignkey.Book(name="The First Demo",pub_date="2018-04-24")
b2= foreignkey.Book(name="The Second Demo",pub_date="2018-04-25")
b3 = foreignkey.Book(name="The Third Demo",pub_date="2018-04-26")
# 创建作者
a1 = foreignkey.Author(name="Futongyong")
a2 = foreignkey.Author(name="Chenwei") 
a3 = foreignkey.Author(name="Xiangjinhu")
# 关联关系
b1.authors = [a1,a3]
b2.authors = [a2,a3]
b3.authors = [a1,a2,a3]

session.add_all([b1,b2,b3,a1,a2,a3])
'''
book_obj = session.query(foreignkey.Book).filter(foreignkey.Book.id==1).first()
author_obj1 = session.query(foreignkey.Author).filter(foreignkey.Author.name=="Futongyong").first()
author_obj2 = session.query(foreignkey.Author).filter(foreignkey.Author.name=="Chenwei").first()
author_obj3 = session.query(foreignkey.Author).filter(foreignkey.Author.name=="Xiangjinhu").first()

book_obj.authors.append(author_obj3)
session.add(book_obj)
session.commit()
session.close()