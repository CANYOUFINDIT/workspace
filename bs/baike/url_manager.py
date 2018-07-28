#coding:utf8
#url管理器

class UrlManager(object):
    def __init__(self):
        #新url列表
        self.new_urls =set()
        #旧url列表
        self.old_urls =set() 

    #向管理器添加新的url
    def add_new_url(self, url):
        #判断url的值是否为空
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            #将url添加到新url列表
            self.new_urls.add(url)

    #向管理器批量添加url
    def add_new_urls(self, urls):
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    #判断是否有新的待爬取的url
    def has_new_url(self):
        #长度不为0则返回True
        return len(self.new_urls) != 0

    #从管理器中获取新的url并添加到旧的url列表中
    def get_new_url(self):
        #pop()方法会从set列表中获取并移除一个url
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)