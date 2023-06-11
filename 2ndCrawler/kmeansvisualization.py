#-*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from  matplotlib import cm
import datetime
import seaborn as sns # 追加
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
strnum = "1000"
dfraw = pd.read_excel("KMeansResult/gamedataResult_k" + strnum + "_new.xlsx",index_col=0)
dfraw['year'] = dfraw.apply(lambda x:str(x['发行日期'])[0:4],axis = 1)
df = dfraw.copy()
df_top1k = dfraw[0:10000].copy()
df_now = dfraw.copy()

df.info()
df.describe()

Y = df_now['近期评价'] # 每一个点的Y值
X = df_now['价格']# 每一个点的X值
sns.set() # 追加
plt.figure(figsize=(30, 5))#大小
#这里散点大小表示评价数量
#颜色取决于好评率高低，colorbar也就是cmap选择'RdYlBu'风格
s1 = sns.stripplot(x=X, y=Y, hue=df_now['游戏属于的簇'],palette="RdYlBu", size=10, jitter=0.95, edgecolor="black", alpha=0.5)
#plt.colorbar().set_label('Group',fontsize=20)
#plt.colorbar(s1, ticks=np.linspace(0,3,4))
plt.xlabel('Price',fontsize=20)
plt.title("k="+strnum)
plt.ylabel('Evaluate',fontsize=20)
plt.show()