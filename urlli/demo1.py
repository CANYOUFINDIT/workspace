# -*- coding: UTF-8 -*-
#网页下载器
import urllib2

#只包含url属性的request对象
request = urllib2.Request("http://www.baidu.com")
#直接请求
response = urllib2.urlopen(request)
#获取状态码，200为获取成功
print response.getcode()
#获取源码
cont = response.read()