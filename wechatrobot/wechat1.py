# -*- coding: UTF-8 -*-
# 自动回复文本消息
import itchat
import re

@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    msg_match = re.match(r'成绩', msg['Text'])# 匹配收到的文本内容，成绩+13位学号+密码
    if msg_match:
        return "There is nothing"
    else:
        return msg['Text']

itchat.auto_login(hotReload=True)
itchat.run()