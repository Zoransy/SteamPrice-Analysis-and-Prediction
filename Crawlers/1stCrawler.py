#尝试爬取steamhistoryprice的popular目录界面
import socket
import urllib.error
import html5lib
import gc
from requests_html import HTMLSession
import json
from urllib import request,parse
import time
import random
from fake_useragent import  UserAgent
from lxml import html
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
#from memory_profiler import profile

#定义一个爬虫类
class SteamSpider(object):
    #初始化url属性
    def __init__(self):
        self.url='https://steampricehistory.com/popular?{}'
        # 添加代理ip
        self.proxies = {
            'http': 'http://61.216.156.222:60808',
            'http': 'http://112.14.47.6:52024',
            'http': 'http://182.139.110.52:9000',
            'http': 'http://117.93.180.175:9000',
            'http': 'http://222.74.73.202:42055',
            'http': 'http://27.42.168.46:55481',
            'http': 'http://27.42.168.46:9000',
            'http': 'http://182.139.110.207:9000',
            'http': 'http://116.9.163.205:58080',
            'http': 'http://61.164.39.68:53281',
            'http': 'http://117.114.149.66:55443',
            'http': 'http://49.85.15.144:9000'
        }
    # 1.请求函数，得到一级页面，传统三步
    def get_html(self,url):
        while True:
            try:
                res = requests.get(url=url, headers={'User-Agent': UserAgent().random}, proxies=self.proxies,
                                   timeout=10)
                break
            except:
                print('timeout')
                time.sleep(1)
        html=res.content.decode('utf-8')
        del res
        gc.collect()
        return html
    # 2.解析函数
    def parse_html(self):
        pass
    # 3.保存文件函数
    def save_html(self,filename,html):
        with open(filename,'w') as f:
            f.write(html)
    # 4.获取二级页面url
    def get_detailurl(self, url):
        #定义前缀
        prefix = "https://steampricehistory.com/app/"
        # 获取网页内容
        while True:
            try:
                response = requests.get(url=url, headers={'User-Agent': UserAgent().random}, proxies=self.proxies, timeout=10)
                break
            except:
                print('timeout')
                time.sleep(1)
        content = response.content
        del response
        gc.collect()
        # 解析HTML
        tree = html.fromstring(content)
        # 提取所有链接
        links = tree.xpath('//a/@href')
        # 过滤出符合前缀的链接
        pattern = re.compile(prefix)
        filtered_links = [link for link in links if pattern.match(link)]
        # 去除URL中的查询参数
        clean_links = [link.split("?")[0] for link in filtered_links]
        # 去除重复元素并存入集合
        unique_links = set(clean_links)
        del tree, links, pattern, filtered_links, clean_links, content
        gc.collect()
        return unique_links
    # 5.提取二级页面表格
    def extract_xlsx(self, url, filename):
        # 异常处理，不知道为什么有时候会读取不到表格所以用死循环实现出现异常时重试
        while True:
            try:
                html = self.get_html(url)
                tables = pd.read_html(html, flavor='bs4')
                del html
                gc.collect()
                break
            except:
                print('Table error')
                time.sleep(1)
        table = tables[1]
        del tables
        gc.collect()
        table["Date"] = pd.to_datetime(table["Date"], format="%B %d, %Y")

        # 将Date列格式化为yyyy-dd-mm的格式
        table["Date"] = table["Date"].dt.strftime("%Y-%m-%d")
        # 替换非法字符
        clfilename = re.sub(r'[\\/:*?"<>|\r\n]+', '_', filename)
        # 使用to_excel方法将表格写入XLS文件
        table.to_excel('PriceData/' + clfilename + ".xlsx", index=False)
        del table, clfilename
        gc.collect()
    # 6.入口函数
    def run(self):
        begin=int(input('输入起始页：'))
        stop=int(input('输入终止页：'))
        # +1 操作保证能够取到整数
        for page in range(begin,stop+1):
            pn=page
            params={
                'page':str(pn)
            }
            #拼接URL地址   
            params=parse.urlencode(params)
            url=self.url.format(params)
            del params
            gc.collect()
            #发请求
            fst_html = self.get_html(url)
            scnd_urls = self.get_detailurl(url)
            print('开始爬取第', pn, '页')
            # 遍历二级页面
            for suburl in scnd_urls:
                while True:
                    try:
                        # 定义模式
                        pattern = "(\d+)"
                        # 使用search方法匹配数字ID
                        match = re.search(pattern, suburl)
                        # 使用group方法获取数字ID
                        id = match.group(1)
                        del match, pattern
                        gc.collect()
                        # 获取游戏名称
                        # 创建一个BeautifulSoup对象
                        soup = BeautifulSoup(fst_html, "html.parser")
                        # 找到a标签
                        a_tags = soup.find_all("a", href=lambda x: x and x.startswith(
                            "https://steampricehistory.com/app/" + id))
                        a_tag = a_tags[1]
                        del soup
                        gc.collect()
                        break
                    except:
                        print('index out of range')
                        time.sleep(1)
                        fst_html = self.get_html(url)
                # 获取a标签中的文本
                del a_tags
                gc.collect()
                text = a_tag.text
                # 定义路径
                filename='{}-{}'.format(id, text)
                print(filename)
                self.extract_xlsx(suburl, filename)
                time.sleep(random.randint(1,2))
                del suburl, id, text, filename, a_tag
                gc.collect()
            del fst_html
            del scnd_urls
            gc.collect()
            print('爬取成功第', pn, '页')
#以脚本的形式启动爬虫
if __name__=='__main__':
    spider=SteamSpider() # 实例化一个对象spider
    spider.run() # 调用入口函数