#coding:utf8
import requests

url = 'http://jwxt.hbnu.edu.cn/jwglxt/cjcx/cjcx_cxDgXscj.html?gnmkdm=N305005&layout=default&su=2016115020429'
cookie = {
    'JSESSIONID': '4FC4253EF798D3CA0017F004B01AECF3',
}
data = {
    'queryModel.showCount': 5,# 返回多少个成绩记录
    'xnm': 2017,# 学年
    'xqm': 1,# 学期（观察post数据，上为3/下为12/全部为空）
}
header = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}# 模拟浏览器

req = requests.post(url=url, headers=header, data=data, cookies=cookie).json()# 获取json数据
req_text = req['items']# 观察得成绩信息在items字段中
print(req_text)