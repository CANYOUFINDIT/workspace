# -*-coding:utf-8-*-
import os
import urllib2

import requests
from bs4 import BeautifulSoup

from models import Student, Subject, Score, db

html = '''
<table>
<tr class="datelisthead">
<td>学年</td><td>学期</td><td>课程代码</td><td>课程名称</td><td>课程性质</td><td>课程归属</td><td>学分</td><td>绩点</td><td>成绩</td><td>辅修标记</td><td>补考成绩</td><td>重修成绩</td><td>学院名称</td><td>备注</td><td>重修标记</td><td>课程英文名称</td>
	</tr><tr>
		<td>2016-2017</td><td>1</td><td>G9902041</td><td>大学生心理健康教育</td><td>必修课</td><td>&nbsp;</td><td>2.0</td><td>   4.30</td><td>93</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>学工处</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr class="alt">
		<td>2016-2017</td><td>1</td><td>TS990101</td><td>大学生职业生涯规划</td><td>必修课</td><td>&nbsp;</td><td>1.0</td><td>   3.45</td><td>84.5</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>就业指导中心</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr>
		<td>2016-2017</td><td>1</td><td>TS030101</td><td>大学英语(一)</td><td>必修课</td><td>&nbsp;</td><td>4.0</td><td>   1.75</td><td>67.5</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>公共外语课部</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr class="alt">
		<td>2016-2017</td><td>1</td><td>HK110101</td><td>高等数学A（一）</td><td>必修课</td><td>&nbsp;</td><td>5.0</td><td>   1.15</td><td>61.5</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>数学与统计学院</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr>
		<td>2016-2017</td><td>1</td><td>Z1501002</td><td>高级语言程序设计</td><td>必修课</td><td>&nbsp;</td><td>5.0</td><td>   2.45</td><td>74.5</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>计算机科学与技术学院</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr class="alt">
		<td>2016-2017</td><td>1</td><td>TS220191</td><td>军事训练与国防教育</td><td>必修课</td><td>&nbsp;</td><td>2</td><td>   3.90</td><td>89</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>军事理论教研室</td><td>&nbsp;</td><td>&nbsp;</td><td></td>
	</tr><tr>
		<td>2016-2017</td><td>1</td><td>TY170002</td><td>排球-俱乐部</td><td>必修课</td><td>体育类</td><td>1.0</td><td>   1.70</td><td>67</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>体育学院</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr class="alt">
		<td>2016-2017</td><td>1</td><td>Z0010105</td><td>普通话训练</td><td>必修课</td><td>&nbsp;</td><td>1.0</td><td>   3.95</td><td>89.5</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>文学院</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr>
		<td>2016-2017</td><td>1</td><td>61010101</td><td>文献信息检索</td><td>必修课</td><td>&nbsp;</td><td>1.0</td><td>   4.60</td><td>96</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>图书馆</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr class="alt">
		<td>2016-2017</td><td>1</td><td>HK110108</td><td>线性代数</td><td>必修课</td><td>&nbsp;</td><td>3.0</td><td>   3.05</td><td>80.5</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>数学与统计学院</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr>
		<td>2016-2017</td><td>1</td><td>TS090105</td><td>形势与政策(一)</td><td>必修课</td><td>&nbsp;</td><td>1.0</td><td>   4.00</td><td>90</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>马克思主义学院</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr class="alt">
		<td>2016-2017</td><td>1</td><td>TS090102</td><td>中国近代史纲要</td><td>必修课</td><td>&nbsp;</td><td>2.0</td><td>   1.65</td><td>66.5</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>马克思主义学院</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr>
		<td>2016-2017</td><td>2</td><td>TS030102</td><td>大学英语(二)</td><td>必修课</td><td>&nbsp;</td><td>4.0</td><td>   1.30</td><td>63</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>公共外语课部</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr class="alt">
		<td>2016-2017</td><td>2</td><td>ZJ150201</td><td>电路分析</td><td>必修课</td><td>&nbsp;</td><td>2.0</td><td>   1.00</td><td>56.5</td><td>0</td><td>60</td><td>&nbsp;</td><td>计算机科学与技术学院</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr>
		<td>2016-2017</td><td>2</td><td>23100004</td><td>电路分析实验</td><td>必修课</td><td>&nbsp;</td><td>1.0</td><td>   4.00</td><td>90</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>电工电子实验示范中心</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr class="alt">
		<td>2016-2017</td><td>2</td><td>23100001</td><td>电子技术实验(A)</td><td>必修课</td><td>&nbsp;</td><td>1.0</td><td>   3.90</td><td>89</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>电工电子实验示范中心</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr>
		<td>2016-2017</td><td>2</td><td>15101615</td><td>电子设计自动化及硬件语言应用</td><td>校公选课</td><td>理科类</td><td>2.0</td><td>   3.75</td><td>87.5</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>计算机科学与技术学院</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr class="alt">
		<td>2016-2017</td><td>2</td><td>HK110102</td><td>高等数学A（二）</td><td>必修课</td><td>&nbsp;</td><td>4.0</td><td>   2.15</td><td>71.5</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>数学与统计学院</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr>
		<td>2016-2017</td><td>2</td><td>ZJ150210</td><td>模拟电子技术基础</td><td>必修课</td><td>&nbsp;</td><td>3.0</td><td>   1.55</td><td>65.5</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>计算机科学与技术学院</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr class="alt">
		<td>2016-2017</td><td>2</td><td>TY170002</td><td>排球-俱乐部</td><td>必修课</td><td>体育类</td><td>1</td><td>   0.00</td><td>47</td><td>0</td><td>50</td><td>&nbsp;</td><td>体育学院</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr>
		<td>2016-2017</td><td>2</td><td>SJ150119</td><td>企业实训（二）</td><td>必修课</td><td>&nbsp;</td><td>2.0</td><td>   3.50</td><td>85</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>计算机科学与技术学院</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr class="alt">
		<td>2016-2017</td><td>2</td><td>TS090101</td><td>思想道德修养与法律基础</td><td>必修课</td><td>&nbsp;</td><td>3.0</td><td>   2.50</td><td>75</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>马克思主义学院</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr>
		<td>2016-2017</td><td>2</td><td>ZY150216</td><td>通信工程制图</td><td>必修课</td><td>&nbsp;</td><td>1.0</td><td>   4.20</td><td>92</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>计算机科学与技术学院</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr class="alt">
		<td>2016-2017</td><td>2</td><td>ZY150215</td><td>通信现代工具</td><td>必修课</td><td>&nbsp;</td><td>2.0</td><td>   4.25</td><td>92.5</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>计算机科学与技术学院</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr>
		<td>2016-2017</td><td>2</td><td>TS090106</td><td>形势与政策(二)</td><td>必修课</td><td>&nbsp;</td><td>1.0</td><td>   4.10</td><td>91</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>马克思主义学院</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr class="alt">
		<td>2017-2018</td><td>1</td><td>ZX150204</td><td>Java面向对象程序设计</td><td>选修课</td><td>&nbsp;</td><td>2.0</td><td>   4.35</td><td>93.5</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>计算机科学与技术学院</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr>
		<td>2017-2018</td><td>1</td><td>TS030103</td><td>大学英语(三)</td><td>必修课</td><td>&nbsp;</td><td>2.0</td><td>   1.00</td><td>51</td><td>0</td><td>60</td><td>&nbsp;</td><td>公共外语课部</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr class="alt">
		<td>2017-2018</td><td>1</td><td>GX030104</td><td>大学英语（拓展课程）</td><td>必修课</td><td>&nbsp;</td><td>2.0</td><td>   3.00</td><td>80</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>公共外语课部</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr>
		<td>2017-2018</td><td>1</td><td>23100002</td><td>电子技术实验(B)</td><td>必修课</td><td>&nbsp;</td><td>1.0</td><td>   3.50</td><td>85</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>电工电子实验示范中心</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr class="alt">
		<td>2017-2018</td><td>1</td><td>HK110111</td><td>概率论与数理统计</td><td>必修课</td><td>&nbsp;</td><td>3.0</td><td>   1.50</td><td>65</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>数学与统计学院</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr>
		<td>2017-2018</td><td>1</td><td>ZJ150211</td><td>工程数学</td><td>必修课</td><td>&nbsp;</td><td>4.0</td><td>   1.75</td><td>67.5</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>计算机科学与技术学院</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr class="alt">
		<td>2017-2018</td><td>1</td><td>ty000018</td><td>乒乓球</td><td>选修课</td><td>&nbsp;</td><td>1.0</td><td>   3.15</td><td>81.5</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr>
		<td>2017-2018</td><td>1</td><td>ZX150201</td><td>数据结构</td><td>选修课</td><td>&nbsp;</td><td>2.0</td><td>   3.95</td><td>89.5</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>计算机科学与技术学院</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr class="alt">
		<td>2017-2018</td><td>1</td><td>SJ150211</td><td>数据结构综合实训</td><td>必修课</td><td>&nbsp;</td><td>3.0</td><td>   3.80</td><td>88</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>计算机科学与技术学院</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr>
		<td>2017-2018</td><td>1</td><td>ZY150217</td><td>数据通信与网络</td><td>必修课</td><td>&nbsp;</td><td>2.0</td><td>   1.25</td><td>62.5</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>计算机科学与技术学院</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr class="alt">
		<td>2017-2018</td><td>1</td><td>ZJ150213</td><td>数字电路与逻辑设计</td><td>必修课</td><td>&nbsp;</td><td>2.0</td><td>   1.00</td><td>55.5</td><td>0</td><td>60</td><td>&nbsp;</td><td>计算机科学与技术学院</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr>
		<td>2017-2018</td><td>1</td><td>SJ150210</td><td>网络与Java程序设计综合实训</td><td>必修课</td><td>&nbsp;</td><td>2</td><td>   4.50</td><td>95</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>计算机科学与技术学院</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr class="alt">
		<td>2017-2018</td><td>1</td><td>22101909</td><td>信息与计算机应用技术</td><td>校公选课</td><td>教育类</td><td>2.0</td><td>   3.75</td><td>87.5</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>计算机科学与技术学院</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr>
		<td>2017-2018</td><td>1</td><td>SJ150216</td><td>学期实训Ⅲ（网络程序设计综合实训） </td><td>必修课</td><td>&nbsp;</td><td>2.0</td><td>   4.10</td><td>91</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>计算机科学与技术学院</td><td>&nbsp;</td><td>0</td><td></td>
	</tr><tr class="alt">
		<td>2017-2018</td><td>2</td><td>TSA07100103</td><td>养生按摩与健康</td><td>校公选课</td><td>&nbsp;</td><td>2</td><td>   0.00</td><td>0</td><td>0</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>0</td><td></td>
	</tr>

</table>'''


def parser(stu_id, html):
    # 根据HTML网页字符串创建BeautifulSoup
    soup = BeautifulSoup(
        html,  # HTML文档字符串
        'html.parser',  # HTML解析器
    )
    stu = Student.query.filter(Student.id == stu_id).first()
    tables = soup.findAll('table')
    tab = tables[0]
    count = 1
    lists = []
    for tr in tab.findAll('tr'):
        if count != 1:
            td = tr.findAll('td')
            for text in td:
                score = text.getText().strip()
                if score == '':
                    score = None
                lists.append(score)
            # 判断课程是否已存在于Subject表中
            sub_obj = Subject.query.filter(
                Subject.class_name == lists[3]).first()
            # 不存在则新插入该课程
            if sub_obj == None:
                sub = Subject(lists[0], lists[1], lists[2], lists[3], lists[4],
                              lists[6], lists[5], lists[9], lists[12], lists[14], lists[15])
                db.session.add(sub)
            # 判断学生没有拥有该课程
            if sub_obj not in stu.subject:
                stu.subject.append(sub)
                db.session.add(stu)
                sub = Subject.query.filter(Subject.class_name == lists[3]).first()
                score = Score(lists[8], lists[7], sub.id,stu_id, lists[10], lists[11], lists[13])
                db.session.add(score)
                db.session.commit()
            # 如果拥有该课程，则更新数据
            else:
                for cla in stu.subject:
                    if cla == sub_obj:
                        cla.score[0].score = lists[8]
                        cla.score[0].GPA = lists[7]
                        cla.score[0].resit_score = lists[10]
                        cla.score[0].restudy_score = lists[11]
                        cla.score[0].note = lists[13]
                        cla.minor_tab = lists[9]
                        cla.resit_tab = lists[14]
                        db.session.commit()
            lists = []
        count = count + 1


parser(2016115020429, html)
