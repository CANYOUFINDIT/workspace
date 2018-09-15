#coding:utf8
#爬虫主程序

import url_manager, html_downloader, html_parser, html_outputer

class SpiderMain(object):
    def __init__(self):
        #url管理器
        self.urls = url_manager.UrlManager()
        #url下载器
        self.downloader = html_downloader.HtmlDownloader()
        #url解析器
        self.parser = html_parser.HtmlParser()
        #ur输出器
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, root_url):
        count = 1
        #添加到新url列表
        self.urls.add_new_url(root_url)
        #当新url列表中还有url时
        while self.urls.has_new_url():
            try:
                #获取新url列表中的url并移除
                new_urls = self.urls.get_new_url()
                print 'craw %d : %s' % (count, new_urls)
                #url对应html网页的内容
                html_cont = self.downloader.download(new_urls)
                new_urls, new_data = self.parser.parse(new_urls, html_cont)
                self.urls.add_new_url(new_urls)
                self.outputer.collect_data(new_data)
                
                if count == 1000:
                    break

                count = count + 1
            except:
                print 'craw failed'

        self.outputer.output_html()

if __name__ == "__main__":
    #入口url
    root_url = "https://nba.hupu.com/"
    obj_spider = SpiderMain()
    #启动爬虫
    obj_spider.craw(root_url)