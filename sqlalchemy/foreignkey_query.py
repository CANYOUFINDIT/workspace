# -*- coding: UTF-8 -*-
# 查询数据
import foreignkey
from sqlalchemy.orm import sessionmaker

Session_class = sessionmaker(bind=foreignkey.engine)  # 创建与数据库的会话session class ,注意,这里返回给session的是个class,不是实例
session = Session_class()  # 生成session实例 #cursor

#查询
#查询作者为Futongyong的书
author_obj = session.query(foreignkey.Author).filter(foreignkey.Author.name=="Futongyong").first()
print(author_obj.books)
#查询id为1的书的作者
book_obj = session.query(foreignkey.Book).filter(foreignkey.Book.id==1).first()
print(book_obj.authors)

session.close()