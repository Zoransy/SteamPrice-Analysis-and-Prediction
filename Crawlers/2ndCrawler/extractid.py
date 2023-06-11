import pandas as pd
import os

# 获取文件夹路径
folder_path = "D:\\Code\\PythonProjects\\1stspider\\PriceData"

# 创建一个空的DataFrame来存储链接和id
df_output = pd.DataFrame(columns=["Link", "ID"])

# 遍历文件夹中的xlsx文件
for file_name in os.listdir(folder_path):
    # 检查文件名是否以xlsx结尾
    if file_name.endswith(".xlsx"):
        # 获取文件名中的id和游戏名，以"-"分割
        id, game_name = file_name.split("-", 1)
        # 生成链接和id两列
        link = "https://store.steampowered.com/app/" + id + "/"
        # 将链接和id添加到输出DataFrame中
        df_output = pd.concat([df_output, pd.DataFrame({"Link": [link], "ID": [id]})], ignore_index=True)

# 创建一个ExcelWriter对象，指定输出文件名
writer = pd.ExcelWriter("urls.xlsx")

# 写入输出DataFrame到工作表中
df_output.to_excel(writer, sheet_name="sheet1", index=False)

# 保存excel文件
writer.close()

