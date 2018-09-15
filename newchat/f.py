# coding:utf-8
from flask import Flask,request,redirect,render_template,session,jsonify
import time
import requests
import re
from bs4 import BeautifulSoup
import json


app = Flask(__name__)
app.secret_key='adfa12da'


def xml_parser(text):
    dic = {}
    soup = BeautifulSoup(text, 'html.parser')
    div = soup.find(name='error')
    for item in div.find_all(recursive=False):
        dic[item.name] = item.text
    return dic


@app.route('/',methods=['GET',"POST"])
def login():
    '''
    扫码获取头像
    :return: 
    '''
    if request.method=='GET':
        ctime = str(int(time.time()*1000))
        qcode_url = 'https://login.wx.qq.com/jslogin?appid=wx782c26e4c19acffb&redirect_uri=https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&fun=new&lang=zh_CN&_={0}'.format(ctime)
        ret = requests.get(qcode_url)
        qcode = re.findall('uuid = "(.*)";',ret.text)[0]
        session['qcode'] = qcode
        session['login_cookies'] = ret.cookies.get_dict()
        return render_template('login.html',qcode=qcode)
    else:
        pass


@app.route('/check_login',methods=['GET','POST'])
def check_login():
    '''
    检测是否已经登录.
    url:https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid=AcjVHfghyA==&tip=0&r=-557419402&_=1529565723654
    :return: 
    '''
    if request.method=='GET':
        response= {'code':408}
        qcode = session.get('qcode')
        ctime = str(int(time.time()*1000))
        check_url = 'https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid={0}&tip=0&r=-557419402&_={1}'.format(qcode,ctime)
        ret = requests.get(url=check_url)
        print(ret.text)
        if 'code=201' in ret.text:
            src = re.findall("userAvatar = '(.*)';",ret.text)[0]
            response['code']=201
            response['src'] = src

        elif 'code=200' in ret.text:
            src = re.findall('redirect_uri="(.*);',ret.text)[0]
            response['code']=200
            response['src']=src
            ret = requests.get(url=src+'&fun=new&version=v2&lang=zh_CN')
            xml_dic = xml_parser(ret.text)
            session['xml_dic']=xml_dic
            session['pass_cookies'] = ret.cookies.get_dict()
            print(xml_dic)
        return jsonify(response)


@app.route('/index',methods=['GET',"POST"])
def index():

    pass_ticket =session['xml_dic'].get('pass_ticket')
    inni_dic={
        'BaseRequest':{
            'DeviceID':"e901523268059245",
            'Sid':session['xml_dic'].get('wxsid'),
            'Skey':session['xml_dic'].get('skey'),
            'Uin':session['xml_dic'].get('wxuin'),
        }
    }
    inni_msg = requests.post(
        url ='https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxinit?r=-581032482&lang=zh_CN&pass_ticket={0}'.format(pass_ticket),
        json=inni_dic
    )
    inni_msg.encoding='utf-8'
    user_dict = inni_msg.json()
    session['user_info'] = user_dict['User']
    session['SyncKey'] = user_dict['SyncKey']


    ctime= str(int(time.time()*1000))
    contact_url= 'https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxgetcontact?lang=zh_CN&pass_ticket={0}&r={1}&seq=0&skey={2}'
    contact_url = contact_url.format(pass_ticket,ctime,session['xml_dic'].get('skey'))
    pass_cookies = session.get('pass_cookies')
    contact_list = requests.get(
        url=contact_url,
        cookies = pass_cookies,
    )
    contact_list.encoding = 'utf-8'
    result_list = contact_list.json()

    return render_template('index.html',user_dict=user_dict,result_list=result_list)


@app.route('/get_img',methods=['GET','POST'])
def get_img():

    # 需要不断的试cookies
    # 登录以后的操作一般都需要cookies, 一般cookies是拿登录成功后的

    # 特殊的需要将cookies成功之后才能进行登录,访问的时候就记录cookies

    # headers的重要参数: Referer host User_Agent

    user_info = session.get('user_info')
    pass_cookies = session.get('pass_cookies')
    header_url = "https://wx2.qq.com"+user_info['HeadImgUrl']
    ret = requests.get(
        url = header_url,
        cookies = pass_cookies,
        headers= {
            'Content-Type': 'image/jpeg',
        }
    )
    return ret.content


@app.route('/send_msg',methods=['GET','POST'])
def send_msg():
    if request.method=='GET':
        return render_template('send.html')
    else:
        data =request.form
        to = data.get('to')
        content = data.get('content')
        print(to,content)
        user = session['user_info']['UserName']
        pass_ticket =session['xml_dic'].get('pass_ticket')
        ctime= str(int(time.time()*1000))
        send_url ='https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxsendmsg?lang=zh_CN&pass_ticket={0}'.format(pass_ticket)

        send_dict = {
            'BaseRequest':{
                'DeviceID': "e901523268059245",
                'Sid': session['xml_dic'].get('wxsid'),
                'Skey': session['xml_dic'].get('skey'),
                'Uin': session['xml_dic'].get('wxuin'),
            },
            'Msg':{'ClientMsgId':ctime,
                   'LocalID':ctime,
                   'FromUserName':user,
                   'ToUserName':to,
                    'Type':1,
                    'Content':content,
            },
            'Scene':0,}

        ret = requests.post(
            url=send_url,
            data=bytes(json.dumps(send_dict,ensure_ascii=False),encoding='utf-8'),
        )

        return ret.text


if __name__ == "__main__":
    app.run(debug=True)