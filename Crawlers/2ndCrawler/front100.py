import json
import time
import random
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from lxml import etree

# 速度优化

chrome_options = Options()
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument('--start-maximized')
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-software-rasterizer")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--allow-running-insecure-content')
chrome_options.add_argument("blink-settings=imagesEnabled=false")

# 事前准备cookies
driver = webdriver.Chrome(options=chrome_options)
driver.set_page_load_timeout(20)  # 页面加载超时时间

driver.set_script_timeout(20)  # 页面js加载超时时间
s = requests.Session()
driver.get('https://store.steampowered.com/')
with open('fullcookies.txt', 'r') as f:
    # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
    cookies_list = json.load(f)
    for cookie in cookies_list:
        driver.add_cookie(cookie)
    driver.refresh()
cookies = driver.get_cookies()
for cookie in cookies:
    s.cookies.set(cookie['name'], cookie['value'])

## 配置headless模型

chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-software-rasterizer")

## 配置不加载图片


chrome_options.add_argument("blink-settings=imagesEnabled=false")

## 禁用插件加载

chrome_options.add_argument("--disable-extensions")


def gamename(soup):  # 游戏名字
    try:
        a = soup.find(class_="apphub_AppName")
        k = str(a.string)
    except:
        a = soup.find(class_="apphub_AppName")
        k = str(a.text)
    return k


def gameprice(soup):  # 价格
    try:
        a = soup.findAll(class_="discount_original_price")
        for i in a:
            if re.search('¥|free|免费', str(i), re.IGNORECASE):
                a = i
        k = str(a.string).replace('	', '').replace('\n', '').replace('\r', '').replace(' ', '')
    except:
        a = soup.findAll(class_="game_purchase_price price")
        for i in a:
            if re.search('¥|free|免费', str(i), re.IGNORECASE):
                a = i
        k = str(a.string).replace('	', '').replace('\n', '').replace('\r', '').replace(' ', '')
    return k


def taglist(soup):  # 标签列表
    list1 = []
    a = soup.find_all(class_="app_tag")
    for i in a:
        k = str(i.string).replace('	', '').replace('\n', '').replace('\r', '')
        if k == '+':
            pass
        else:
            list1.append(k)
    list1 = str('\n'.join(list1))
    return list1


def description(soup):  # 游戏描述
    a = soup.find(class_="game_description_snippet")
    k = str(a.string).replace('	', '').replace('\n', '').replace('\r', '')
    return k


def reviewsummary(soup):  # 总体评价
    a = soup.find(class_="summary column")
    try:
        k = str(a.span.string)
    except:
        k = str(a.text)
    return k


def getdate(soup):  # 发行日期
    a = soup.find(class_="date")
    k = str(a.string)
    return k


def userreviewsrate(soup):  # 总体数量好评率
    # a = soup.find(class_="user_reviews_summary_row")
    # k = str(a.attrs['data-tooltip-html'])
    # return k


    # span = soup.find('span', class_='nonresponsive_hidden responsive_reviewdesc')  # 根据class属性找到span标签
    # if span:  # 如果找到了span标签
    #     text = span.get_text(strip=True)  # 提取span标签中的文字，并去掉空白字符
    #     return text  # 返回文字
    # else:  # 如果没有找到span标签
    #     return None  # 返回None
    tree = etree.HTML(soup)  # 将网页转换为HTML树
    xpaths = [
        '/html/body/div[1]/div[7]/div[6]/div[3]/div[2]/div[1]/div[4]/div[1]/div[2]/div[1]/div/div[3]/div[1]/div[2]/div[2]/span[3]/text()',
        '/html/body/div[1]/div[7]/div[6]/div[3]/div[2]/div[1]/div[4]/div[1]/div[2]/div[2]/div/div[3]/div[1]/div[2]/div[2]/span[3]/text()',
        '/html/body/div[1]/div[7]/div[6]/div[3]/div[2]/div[1]/div[4]/div[1]/div[2]/div[1]/div/div[3]/div[1]/div/div[2]/span[3]/text()']  # 定义一个列表，存储可能需要的xpath表达式
    for xpath in xpaths:  # 使用一个循环，遍历这个列表
        span = tree.xpath(xpath)  # 通过xpath找到span标签
        if span:  # 如果找到了span标签
            return span  # 返回文本内容
    return None  # 如果没有找到任何文本内容，返回None


def isdlc(soup):  # 判断是否为DLC
    try:
        a = soup.find(class_="game_area_bubble game_area_dlc_bubble")
        t = a.text
        return True
    except:
        return False


def getdlctext(soup):  # 获取DLC信息
    div = soup.find(class_="game_area_bubble game_area_dlc_bubble")
    p = div.find("p")
    result = p.text.strip()
    return result


def developer(soup):  # 开发商
    a = soup.find(id="developers_list")
    k = str(a.a.string)
    return k


def getreviews(ID):  # 获取评论
    r1 = s.get(
        'https://store.steampowered.com/appreviews/%s?cursor=*&day_range=30&start_date=-1&end_date=-1&date_range_type=all&filter=summary&language=schinese&l=schinese&review_type=all&purchase_type=all&playtime_filter_min=0&playtime_filter_max=0&filter_offtopic_activity=1' % str(
            ID), headers={'User-Agent': UserAgent().random}, timeout=10)
    soup = BeautifulSoup(r1.json()['html'], 'lxml')
    a = soup.findAll(class_="content")
    list1 = []
    for i in a:
        list1.append(i.text.replace('	', '').replace('\n', '').replace('\r', '').replace(' ', ','))
    k = str('\n'.join(list1))
    return k


def getdetail(x):
    tag, des, reviews, date, rate, dev, review, name, price = ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '
    global count
    ct = 0
    while ct < 3:
        try:
            r = s.get(x['Link'], headers={'User-Agent': UserAgent().random}, timeout=10)
            soup = BeautifulSoup(r.text, 'lxml')
            if not (soup.find("a", id="view_product_page_btn") is None):
                driver.get(x['Link'])
                print("find success")
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='view_product_page_btn']")))
                button.click()
                html = driver.page_source
                soup = BeautifulSoup(html, "lxml")
            if not isdlc(soup):
                print("isgame")
                name = gamename(soup)
                tag = taglist(soup)
                des = description(soup)
                reviews = reviewsummary(soup)
                date = getdate(soup)
                rate = userreviewsrate(str(soup))
                dev = developer(soup)
                review = getreviews(str(x['ID']))
                # = gameprice(soup)
                print('已完成: ' + name + " " + str(x['ID']) + ' 第%d个' % count)
            else:
                print("isdlc")
                name = gamename(soup)
                tag = taglist(soup)
                des = getdlctext(soup)
                reviews = reviewsummary(soup)
                date = getdate(soup)
                rate = userreviewsrate(str(soup))
                dev = developer(soup)
                review = getreviews(str(x['ID']))
                #price = gameprice(soup)
                print('已完成: ' + name + " " + str(x['ID']) + ' 第%d个' % count + " 该游戏为dlc")
            ''' r.encoding = r.apparent_encoding
            with open("success.html", "w", encoding='utf-8') as f:
                f.write(r.text)'''
            break
        except Exception as e1:
            try:
                driver.refresh()
            except Exception as e3:
                print(e3)
            print('未完成:  ' + str(x['ID']) + '第%d个' % count)
            print(e1)
            # 还是生日验证的问题，需要加载chrome的cookies
            # with open("errorpages/" + str(x['ID']) + ".html", "w", encoding='utf-8') as f:
            #     try:
            #         f.write(html)
            #     except Exception as e2:
            #         print(e2)
            #         print("write page failed")
            r.encoding = r.apparent_encoding
            with open("errorpages/" + str(x['ID']) + ".html", "w", encoding='utf-8') as f:
                try:
                    f.write(r.text)
                except Exception as e2:
                    print(e2)
                    print("write page failed")

            ct = ct + 1
    count += 1
    return name, tag, des, reviews, date, rate, dev, review


if __name__ == "__main__":
    df1 = pd.read_excel('100.xlsx')
    count = 1
    df1['详细'] = df1.apply(lambda x: getdetail(x), axis=1)
    df1['名字'] = df1.apply(lambda x: x['详细'][0], axis=1)
    #df1['价格'] = df1.apply(lambda x: x['详细'][1], axis=1)
    df1['标签'] = df1.apply(lambda x: x['详细'][1], axis=1)
    df1['描述'] = df1.apply(lambda x: x['详细'][2], axis=1)
    df1['近期评价'] = df1.apply(lambda x: x['详细'][3], axis=1)
    df1['发行日期'] = df1.apply(lambda x: x['详细'][4], axis=1)
    df1['总体数量好评率'] = df1.apply(lambda x: x['详细'][5], axis=1)
    df1['开发商'] = df1.apply(lambda x: x['详细'][6], axis=1)
    df1['评论'] = df1.apply(lambda x: x['详细'][7], axis=1)
    df1.drop(df1.columns[2], axis=1, inplace=True)
    df1.to_excel('result100.xlsx')
    driver.close()
    print('已完成全部')
