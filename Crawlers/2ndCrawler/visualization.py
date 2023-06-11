import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from  matplotlib import cm
import datetime
import seaborn as sns # 追加
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

dfraw = pd.read_excel("results_with_comments_and_prices_cl_visual_final.xlsx",index_col=0)
dfraw['year'] = dfraw.apply(lambda x:str(x['发行日期'])[0:4],axis = 1)
df = dfraw.copy()
df_top1k = dfraw[0:10000].copy()
df_now = dfraw[dfraw['评价数量'].values!=0].copy()

df.info()
df.describe()

Y = df_now['价格'] # 每一个点的Y值
X = df_now['发行日期']# 每一个点的X值
sns.set() # 追加
plt.figure(figsize=(20, 5))#大小
#这里散点大小表示评价数量
#价格是美元，这里按照RMB进行绘图所以*7
#颜色取决于好评率高低，colorbar也就是cmap选择'RdYlBu'风格
plt.scatter(X,Y*7, s=df_now["评价数量"]/200, c=df_now['好评率'], alpha=.9,cmap=plt.get_cmap('RdYlBu'))
plt.colorbar().set_label('Game_Review',fontsize=20)
plt.ylim(0, 1500)
plt.xlabel('Year',fontsize=20)
plt.ylabel('Price',fontsize=20)
plt.show()

Y = df_now['价格'] # 每一个点的Y值
X = df_now['发行日期']# 每一个点的X值
sns.set() # 追加
plt.rcParams['font.sans-serif']=['Microsoft YaHei']#字体
plt.figure(figsize=(20, 5))#大小
#这里散点大小表示评价数量
#颜色取决于好评率高低，colorbar也就是cmap选择'RdYlBu'风格
plt.scatter(X,Y*7, s= df_now["评价数量"]/200, c=df_now['好评率'], alpha=.9,cmap=plt.get_cmap('RdYlBu'))
datenow = datetime.datetime(2021,1,1)
dstart = datetime.datetime(2007,1,1)
plt.xlim(dstart, datenow)
plt.ylim(0, 500)
plt.xlabel('Year',fontsize=20)
plt.ylabel('Price',fontsize=20)
plt.colorbar().set_label('Game_Review',fontsize=20)
plt.show()

df_yearprice = df.groupby('year')['价格'].mean().to_frame().reset_index().sort_values(by='year')#按年分组，求平均价格
df_yearreview = df.groupby('year')['好评率'].mean().to_frame().reset_index().sort_values(by='year')#按年分组，求平均好评率

plt.figure(figsize=(20, 5))
plt.plot(df_yearreview['year'],df_yearreview['好评率'], c='g',label='平均好评率%')
plt.plot(df_yearprice['year'],df_yearprice['价格'], c='c',label='平均价格')
plt.xlabel('Year',fontsize=20)
plt.legend()
plt.title('Year and Price and Game_Review')
plt.xlim(4,35)
plt.ylim(0, 100)
plt.show()

list1 = []
list1 = df['标签'].to_list()#全部一万个

list1 = '\n'.join(list1)
list1 =list1.split('\n')#把所有标签加入list1
frequency = {}
frequency1 = {}
for word in list1:#词频统计
    if word not in frequency:
        frequency[word] = 1
    else:
        frequency[word] += 1
frequency = sorted(frequency.items(),key = lambda x :x[1], reverse=True)#根据词频降序做排列输出一个元组
for i in frequency:
    print(i[0])
    frequency1[str(i[0])[0:4]+'\n'+str(i[0])[4:8]+'\n'+str(i[0])[8:12]+'\n'+str(i[0])[12:16]]=i[1]#元组转为字典，再让标签每隔2个字加\n,后面柱状图会用到
dffre = df.copy()
for i in  list(frequency)[0:50]:#检验50个tag覆盖率
    dffre = dffre[dffre['标签'].str.contains(i[0])== False]

print(len(dffre))

Y = list(frequency1.keys())[0:50]#取前50个标签
X = list(frequency1.values())[0:50]
plt.figure( figsize=(20, 5),)

plt.bar(Y,X, facecolor='#ff9999', edgecolor='white')

plt.xlabel('游戏类型',fontsize=20)
plt.ylabel('游戏数量',fontsize=20)
plt.xlim(-.5, 49.5)
for a,b in zip(Y,X):
    plt.text(a, b,int(b), ha='center', va= 'bottom',fontsize=10)
plt.show()

