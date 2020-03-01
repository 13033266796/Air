import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from statsmodels.tsa.api import ExponentialSmoothing
from sklearn.metrics import mean_squared_error
import os

# 获取所有城市的数据文件名并存为一个列表
# city_filename_list = os.listdir(r"./city_all_data")
#
# city_rmse = dict()

# 遍历所有的文件名并读取进行预测
# for city_filename in city_filename_list:
#     # 提取城市名
#     city_name = city_filename.split("_")[0]
#
#     # 读取数据并将AQI这列分离成以时间序列为index的series对象
#     original_data = pd.read_csv(r"./city_all_data/" + city_filename)
#     original_data.timestamp = pd.to_datetime(original_data["month"].values, format="%Y-%m")
#     original_data.index = original_data.timestamp
#     original_data["AQI"] = original_data["AQI"].round(decimals=2)
#
#     # 三指数平滑模型拟合
#     # 创建一个形状和源数据一样，12行的DataFrame对象，用于存储预测数据，同时方便拼接数据
#     predict_data = pd.DataFrame(original_data[:12].copy())
#     time_index = pd.date_range("2019-12", "2020-11", freq="MS")
#     predict_data.index = pd.to_datetime(time_index)
#     predict_data["month"] = ["2019-12", "2020-01", "2020-02", "2020-03", "2020-04",
#                              "2020-05", "2020-06", "2020-07", "2020-08", "2020-09",
#                              "2020-10", "2020-11"]
#     fit1 = ExponentialSmoothing(np.asarray(original_data["AQI"]),
#                                 seasonal_periods=12, trend="add", seasonal="add").fit()
#     predict_data["AQI"] = fit1.forecast(len(predict_data))  # 从2019-12开始往后预测12个月
#     predict_data["AQI"] = predict_data["AQI"].round(decimals=2)
#
#     # 拼接为一个数据源
#     concat_data = pd.concat([original_data, predict_data])
#
#     # 所有城市的预测数据存储为csv文件
#     file_name = city_name + "市AQI预测数据.csv"
#     concat_data[["city_name", "month", "AQI"]].to_csv(r"./time_series_predict_AQI/" + file_name, index=False)
#
#     # 计算拟合度并存储
#     rms = math.sqrt(mean_squared_error(original_data.AQI[59:], predict_data.AQI))
#     city_rmse[city_name] = rms
#
#     # 绘图
#     plt.figure(figsize=(16, 8))
#     plt.plot(concat_data["AQI"], label="Concat_Data", color="blue")   # 拼接数据
#     plt.plot(original_data["AQI"], label="Original", color="red")   # 原数据
#     plt.plot(predict_data["AQI"], label="Holt_Winter", color="green")    # 预测数据
#     plt.legend(loc="best")
#     plt.title(city_name + "市2014-2019年AQI折线图及对2020年的预测->RMSE:%.2f" % rms)
#     plt.savefig(r"./predict_image/AQI/" + city_name + "市AQI.png")
#     plt.show()


# print(city_rmse)

# 读取数据并将AQI这列分离成以时间序列为index的series对象
# original_data = pd.read_csv(r"./city_all_data/" + city_filename)
original_data = pd.read_csv(r"../Province_data/original/上海_2year_data.csv")
original_data.timestamp = pd.to_datetime(original_data["day"].values, format="%Y-%m-%d")
original_data.index = original_data.timestamp
original_data["AQI"] = original_data["AQI"].round(decimals=2)
# print(original_data["AQI"])
# plt.plot(original_data["AQI"])
# plt.show()

# 三指数平滑模型拟合
# 创建一个形状和源数据一样，12行的DataFrame对象，用于存储预测数据，同时方便拼接数据
# predict_data = pd.DataFrame(original_data[:12].copy())
# time_index = pd.date_range("2019-12", "2020-11", freq="MS")
# predict_data.index = pd.to_datetime(time_index)
# predict_data["month"] = ["2019-12", "2020-01", "2020-02", "2020-03", "2020-04",
#                          "2020-05", "2020-06", "2020-07", "2020-08", "2020-09",
#                          "2020-10", "2020-11"]
fit1 = ExponentialSmoothing(np.asarray(original_data["AQI"]),
                            seasonal_periods=30, trend="add", seasonal="add").fit()
res = fit1.forecast(20)
# print(res)
predict_data = pd.Series(res)
predict_data.index = pd.date_range("20200101","20200120",freq="D")
print(predict_data)
concat_data = pd.concat([original_data["AQI"], predict_data.round(decimals=2)])
print(concat_data)
# predict_data["AQI"] = fit1.forecast(len(predict_data))  # 从2019-12开始往后预测12个月
# predict_data["AQI"] = predict_data["AQI"].round(decimals=2)
#
# # 拼接为一个数据源
# concat_data = pd.concat([original_data, predict_data])
#
# # 所有城市的预测数据存储为csv文件
# file_name = city_name + "市AQI预测数据.csv"
# concat_data[["city_name", "month", "AQI"]].to_csv(r"./time_series_predict_AQI/" + file_name, index=False)
#
# 计算拟合度并存储
rms = math.sqrt(mean_squared_error(original_data.AQI[710:], predict_data.values))
print(rms)
#
# # 绘图
plt.figure(figsize=(16, 8))
plt.plot(concat_data, label="Concat_Data", color="blue")   # 拼接数据
plt.plot(original_data["AQI"], label="Original", color="red")   # 原数据
plt.plot(predict_data, label="Holt_Winter", color="green")    # 预测数据
plt.legend(loc="best")
plt.title("上海" + "市2014-2019年AQI折线图及对2020年的预测->RMSE:%.2f" % rms)
# plt.savefig(r"./predict_image/AQI/" + city_name + "市AQI.png")
plt.show()