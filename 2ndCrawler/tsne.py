# 导入相关库
import numpy as np
import matplotlib.pyplot as plt
from sklearn import manifold
import pandas as pd

# 读取xlsx文件，指定列名为"价格"、"标签"、"好评率"，指定想要读取的列名为这三列
data = pd.read_excel(io="gamedataResult_k100.xlsx", names=["价格", "标签", "好评率", "游戏属于的簇"], usecols=["价格", "标签", "好评率", "游戏属于的簇"])

# 提取特征和标签
X = data[["价格", "标签", "好评率"]] # 取前三列作为特征
y = data["游戏属于的簇"] # 取最后一列作为标签
print(X)
# 初始化t-SNE模型
tsne = manifold.TSNE(n_components=2, perplexity=30, learning_rate=200)

# 转换高维数据为低维数据，不需要提供簇中心数据
X_tsne = tsne.fit_transform(X)

# 绘制散点图
plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=y, cmap="rainbow")
plt.colorbar()
plt.xlabel("Dimension 1")
plt.ylabel("Dimension 2")
plt.title("t-SNE Visualization")

# 显示图形
plt.show()
