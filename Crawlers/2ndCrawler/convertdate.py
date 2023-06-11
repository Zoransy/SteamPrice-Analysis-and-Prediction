# 导入pandas库
import pandas as pd
import re

# 读取result100.xlsx文件
df = pd.read_excel("results_with_comments_and_prices_cl.xlsx")
print(df.info())

# 把"发行日期"列转换为datetime64格式
df["发行日期"] = pd.to_datetime(df["发行日期"], format="mixed")




def price(x):
    try:
        pricenum = int(x['价格'].replace('$', ''))
    except:
        pricenum = 0
    return pricenum


def getreviewsnum(x):
    x = x['近期数量好评率']
    if re.search('(\d*%) of the (\d+(,\d+)*) user reviews in the last 30 days are positive.', x):
        rate = re.search('(\d*%) of the (\d+(,\d+)*) user reviews in the last 30 days are positive.', x).group(2)
    elif re.search('(\d*%) of the (\d+(,\d+)*) user reviews for this \w+ are positive.', x):
        rate = re.search('(\d*%) of the (\d+(,\d+)*) user reviews for this \w+ are positive.', x).group(2)
    else:
        rate = ''
    return rate

def getreviewsrate(x):
    x1 = x['近期数量好评率']
    x2 = x['近期评价']
    if re.search('(\d*%) of the (\d+(,\d+)*) user reviews in the last 30 days are positive.', x1):
        num = re.search('(\d*%) of the (\d+(,\d+)*) user reviews in the last 30 days are positive.', x1).group(1)
    elif re.search('(\d*%) of the (\d+(,\d+)*) user reviews for this \w+ are positive.', x1):
        num = re.search('(\d*%) of the (\d+(,\d+)*) user reviews for this \w+ are positive.', x1).group(1)
    elif re.search('(\d*) user reviews', x2):
        num = re.search('(\d*) user reviews', x2).group(1)
    else:
        num = '0'
    return num
# df['价格'] = df.apply(lambda x: price(x), axis=1)
# df['价格'] = pd.to_numeric(df['价格'])  # 转为int64
df['评价数量'] = df.apply(lambda x: getreviewsnum(x), axis=1)
df['好评率'] = df.apply(lambda x: getreviewsrate(x), axis=1)
df['评价数量'] = df['评价数量'].apply(lambda x: x.replace(',', ''))
df['好评率'] = df['好评率'].apply(lambda x: str(x).replace('%', ''))
df['评价数量'] = pd.to_numeric(df['评价数量'])
df['好评率'] = pd.to_numeric(df['好评率'])
df['ID'] = df['ID'].astype('str')  # 这里顺路把ID转为str
df.to_excel("results_with_comments_and_prices_cl_visual.xlsx", index=False)
