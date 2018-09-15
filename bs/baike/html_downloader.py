#coding:utf8
#html下载器

import urllib2

class HtmlDownloader(object):

    def download(self, url):
        if url is None:
            return None

        #请求下载url对应的网页
        response = urllib2.urlopen(url)
        
        #查看状态码
        if response.getcode() != 200:
            return None

        #返回html内容
        return response.read()