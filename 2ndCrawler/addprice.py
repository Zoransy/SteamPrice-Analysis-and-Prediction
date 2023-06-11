# 导入pandas模块
import pandas as pd
# 导入os模块
import os

# 读取result.xlsx文件
df = pd.read_excel("results_with_comments.xlsx")

# 创建一个空列表，用于存储价格最大值
price_list = []

# 遍历ID列的每个值
for id in df["ID"]:
    # 拼接PriceData文件夹的路径
    price_dir = "PriceData"
    # 遍历PriceData文件夹中的每个文件名
    for file in os.listdir(price_dir):
        # 如果文件名以id开头，说明是对应的文件
        if file.startswith(str(id)):
            # 拼接文件的完整路径
            file_path = os.path.join(price_dir, file)
            # 读取文件中的Price列，并求最大值
            max_price = pd.read_excel(file_path)["Price"].max()
            # 将最大值添加到价格列表中
            price_list.append(max_price)
            # 跳出循环，继续下一个ID值的匹配
            break

# 将价格列表转换为Series对象，并添加到result.xlsx文件中，命名为"价格"
df["价格"] = pd.Series(price_list)

# 保存修改后的文件
df.to_excel("results_with_comments_and_prices.xlsx", index=False)
