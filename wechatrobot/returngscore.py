# coding:utf-8
import itchat
import time
import requests
import hashlib
import re

def query_grades(a,b,c,d):
    return "There is nothing"

def get_response(msg, FromUserName):
    msg_match = re.match(r'^成绩(\d{13})(.*)$', msg)# 匹配收到的文本内容，成绩+13位学号+密码
    if msg_match: # 如果能匹配的话
        username = msg_match.group(1) # 13位学号
        password = msg_match.group(2) # 后面是密码
        return query_grades(username, password, 2017, 1) # 调用查分函数，查2017年第一学期额成绩

@itchat.msg_register(['Text'])
def Response(msg):
    response = get_response(msg['Content'], msg['FromUserName'])# 获取回复内容
    #itchat.send(response, msg['FromUserName']) # itchat回复
    return response

itchat.auto_login()
itchat.run()