# 导入所需的模块
import pandas as pd
import os

# 定义一个字典，将近期评价的字符串映射为整数
review_dict = {
    "Overwhelmingly Negative": 1,
    "Very Negative": 2,
    "Mostly Negative": 3,
    "Mixed": 4,
    "Mostly Positive": 5,
    "Very Positive": 6,
    "Positive": 6,
    "Overwhelmingly Positive": 7
}

# 遍历KMeansResult文件夹中的所有以gamedataResult开头的xlsx文件
for file in os.listdir("KMeansResult"):
    if file.startswith("gamedataResult") and file.endswith(".xlsx"):
        # 读取文件为DataFrame对象
        df = pd.read_excel(os.path.join("KMeansResult", file))
        # 判断是否有近期评价这一列
        if "近期评价" in df.columns:
            # 将近期评价这一列的值替换为对应的整数
            df["近期评价"] = df["近期评价"].replace(review_dict)
            # 将近期评价这一列的类型转换为数字类型
            df["近期评价"] = pd.to_numeric(df["近期评价"])
            # 将修改后的DataFrame对象保存为新的xlsx文件，文件名加上_new后缀
            df.to_excel(os.path.join("KMeansResult", file[:-5] + "_new.xlsx"), index=False)
