import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from fake_useragent import UserAgent
import openpyxl
# headers = {
#     'Accept': '',
#     'Accept-Encoding': '',
#     'Accept-Language': '',
#     'Cache-Control': '',
#     'Connection': '',
#     'Cookie':'',
#     'Host': '',
#     'Sec-Fetch-Mode': '',
#     'Sec-Fetch-Site': '',
#     'Sec-Fetch-User': '',
#     'Upgrade-Insecure-Requests': '',
#     'User-Agent': ''
# }
#替换你自己的headers
n = 20
#n代表爬取到多少页
path = '1.xlsx'
#修改你的保存位置

def getgamelist(n):
    linklist=[]
    IDlist = []
    for pagenum in range(1,n):
        r = requests.get('https://store.steampowered.com/search/?ignore_preferences=1&category1=998&os=win&filter=globaltopsellers&page=%d'%pagenum,headers={'User-Agent': UserAgent().random})
        soup = BeautifulSoup(r.text, 'lxml')
        soups= soup.find_all(href=re.compile(r"https://store.steampowered.com/app/"),class_="search_result_row ds_collapse_flag")
        for i in soups:
            i = i.attrs
            i = i['href']
            link = re.search('https://store.steampowered.com/app/(\d*?)/',i).group()
            ID = re.search('https://store.steampowered.com/app/(\d*?)/(.*?)/', i).group(1)
            linklist.append(link)
            IDlist.append(ID)
        print('已完成'+str(pagenum)+'页,目前共'+str(len(linklist)))
    return linklist,IDlist

def getdf(n):#转df
    linklist,IDlist = getgamelist(n)
    df = pd.DataFrame(list(zip(linklist,IDlist)),
               columns =['Link', 'ID'])
    return df
if __name__ == "__main__":
    df = getdf(n)#n代表爬取到多少页
    df.to_excel(path)#储存