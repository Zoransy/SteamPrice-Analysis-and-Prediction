# 导入pandas模块
import pandas as pd

# 读取xlsx文件
df = pd.read_excel("gamedataResult_k100.xlsx")
'''
df = df.astype("object")




#df['价格'] = df.apply(lambda x: price(x), axis=1)
df["价格"] = df["价格"].str.replace("$", "")
df['价格'] = pd.to_numeric(df['价格'])  # 转为int64
# #df['评价数量'] = df['评价数量'].apply(lambda x: x.replace(',', ''))
# #df['好评率'] = df['好评率'].apply(lambda x: str(x).replace('%', ''))
#df['ID'] = df['ID'].astype('object')  # 这里顺路把ID转为str
df["发行日期"] = pd.to_datetime(df["发行日期"], format="mixed")
df['评价数量'] = pd.to_numeric(df['评价数量'])
df['好评率'] = pd.to_numeric(df['好评率'])
#df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

#df.dropna(axis=0, inplace=True)
df.describe()
df.info()
'''
df.to_excel("gamedataResult_k100.xlsx", index=True)