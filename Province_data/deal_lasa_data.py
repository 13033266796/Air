import os
import re

with open(r"F:\Python\pyCollect\Air_predict\Provice_data/original/ShangHai_2_year_data.txt","r",encoding="utf-8") as f:
    data = f.readline()
    line = 0
    text = ""
    while data:
        line += 1
        if line == 4:
            res = re.findall(r"\S+", text)
            with open(r"./original/上海_2year_data.csv","a",encoding="utf-8") as t:
                t.write("上海,"+",".join(res)+"\n")
            # print("***", text, "***")
            text = ""
            line = 1
        data = data.strip()
        text += " " + data
        data = f.readline()


    # data = data.strip()
    # print(data)
    # data = f.readline()
    # data = data.strip()
    # print(data)
    # data = f.readline()
    # data = data.strip()
    # print(data)
    # print(text)
    # res = re.findall(r"\S+",text)
    # print(res)
