# -*- coding: UTF-8 -*-
import urllib2

#创建Request对象
request = urllib2.Request("http://www.baidu.com")

#添加数据
request.add_data('a')
request.add_data('1')


#添加http的header，伪装成Mozilla浏览器
request.add_header('User-Agent', 'Mozilla/5.0')

#发送请求获取结果
response = urllib2.urlopen(request)

#获取状态码，200为获取成功
print response.getcode()