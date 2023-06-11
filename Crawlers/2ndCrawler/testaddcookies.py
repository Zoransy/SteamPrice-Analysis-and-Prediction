from selenium import webdriver
import time
import json

# 填写webdriver的保存目录
driver = webdriver.Chrome()

# 记得写完整的url 包括http和https
driver.get('https://store.steampowered.com/')

# 首先清除由于浏览器打开已有的cookies
driver.delete_all_cookies()

with open('cookies.txt','r') as f:
    # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
    cookies_list = json.load(f)
    for cookie in cookies_list:
        driver.add_cookie(cookie)
    driver.refresh()
time.sleep(60)
with open('fullcookies.txt', 'w') as f:
    # 将cookies保存为json格式
    f.write(json.dumps(driver.get_cookies()))