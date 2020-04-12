import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pymysql
from statsmodels.tsa.api import ExponentialSmoothing
from sklearn.metrics import mean_squared_error
from order_time import date_offset
import datetime
from datetime import timedelta

def conn_mysql(city = "北京"):
    conn = pymysql.connect(host='47.115.24.101', port=3306, user='root', passwd='123456', db='show_air',
                           charset='utf8')
    cursor1 = conn.cursor()
    sql = '''
            SELECT city_name, city_date, city_AQI, city_PM2_5 
            FROM display_app_airinfo 
            WHERE city_name="%s"
          ''' % (city)  # 插入数据
    cursor1.execute(sql)
    ret = cursor1.fetchall()  # 元组 (('北京', datetime.date(2013, 12, 2), Decimal('142.00'), Decimal('109.00')), )

    city_data = [[data[0], data[1].strftime('%Y-%m-%d'), float(data[2]), float(data[3])] for data in ret]
    # print(city_data)

    cursor1.close()
    conn.close()

    return np.array(city_data)

def save_to_mysql(dataset):
    conn = pymysql.connect(host='192.168.78.128', port=3306, user='root', passwd='123456', db='show_air',
                           charset='utf8')
    cursor1 = conn.cursor()
    try:
        for data in dataset:
            sql = '''
                    INSERT INTO display_app_predictinfo
                    (city_name, city_date, city_AQI, city_PM2_5)
                    VALUES("%s","%s","%s", "%s")
                  '''%(data[0], data[1], data[2], data[3]) # 查一个城市信息中是否含有重复值
            cursor1.execute(sql)
        conn.commit()
    except Exception as e :
        print(e)
        conn.rollback()
    finally:
        cursor1.close()
        conn.close()


def predict_aqi():
    data = conn_mysql(city="南昌")
    # print(data)
    df = pd.DataFrame(data, columns=["city","date","aqi","pm2_5"])

    df.index = pd.to_datetime(df["date"].values, format="%Y-%m-%d")
    df["aqi"] = df["aqi"].astype("float").round(decimals=2)
    df = df.sort_index()
    # print(df["aqi"])

    fit1 = ExponentialSmoothing(np.asarray(df["aqi"]),
                                seasonal_periods=12, trend="add", seasonal="add").fit()
    res = fit1.forecast(7)
    # print(res)
    predict_data = pd.Series(res)
    predict_data.index = pd.date_range("20200411", "20200417", freq="D")
    print(predict_data)
    concat_data = pd.concat([df["aqi"], predict_data.round(decimals=2)])
    rms = math.sqrt(mean_squared_error(df.aqi[2315:], predict_data.values))
    print(rms)
    #
    # # 绘图
    plt.figure(figsize=(16, 8))
    # plt.plot(concat_data, label="Concat_Data", color="blue")  # 拼接数据
    plt.plot(df["aqi"][-100:-1], label="Original", color="red")  # 原数据
    plt.plot(predict_data, label="Holt_Winter", color="green")  # 预测数据
    plt.legend(loc="best")
    plt.title("南昌" + "市2014-2019年AQI折线图及对2020年的预测->RMSE:%.2f" % rms)
    plt.show()


def predict_pm2_5():
    data = conn_mysql(city="南昌")
    # print(data)
    df = pd.DataFrame(data, columns=["city", "date", "aqi", "pm2_5"])

    df.index = pd.to_datetime(df["date"].values, format="%Y-%m-%d")
    df["pm2_5"] = df["pm2_5"].astype("float").round(decimals=2)
    df = df.sort_index()
    # print(df["pm2_5"])

    fit1 = ExponentialSmoothing(np.asarray(df["pm2_5"]),
                                seasonal_periods=12, trend="add", seasonal="add").fit()
    res = fit1.forecast(7)
    # print(res)
    predict_data = pd.Series(res)
    predict_data.index = pd.date_range("20200101", "20200107", freq="D")
    print(predict_data)
    concat_data = pd.concat([df["pm2_5"], predict_data.round(decimals=2)])
    rms = math.sqrt(mean_squared_error(df.pm2_5[2215:], predict_data.values))
    print(rms)
    
    # # 绘图
    plt.figure(figsize=(16, 8))
    plt.plot(concat_data, label="Concat_Data", color="blue")  # 拼接数据
    plt.plot(df["pm2_5"], label="Original", color="red")  # 原数据
    plt.plot(predict_data, label="Holt_Winter", color="green")  # 预测数据
    plt.legend(loc="best")
    plt.title("南昌" + "市2014-2019年pm2_5折线图及对2020年的预测->RMSE:%.2f" % rms)
    plt.show()
    

def predict_air(city, date):
    data = conn_mysql(city=city)
    df = pd.DataFrame(data, columns=["city", "date", "aqi", "pm2_5"])

    df.index = pd.to_datetime(df["date"].values, format="%Y-%m-%d")
    df["aqi"] = df["aqi"].astype("float").round(decimals=2)
    df["pm2_5"] = df["pm2_5"].astype("float").round(decimals=2)
    df = df.sort_index()

    fit_aqi = ExponentialSmoothing(np.asarray(df["aqi"]),
                                     seasonal_periods=12, trend="add", seasonal="add").fit()
    fit_pm2_5 = ExponentialSmoothing(np.asarray(df["pm2_5"]),
                                     seasonal_periods=12, trend="add", seasonal="add").fit()
    res_aqi = fit_aqi.forecast(7)
    res_pm2_5 = fit_pm2_5.forecast(7)
    # print(res)
    predict_aqi = pd.Series(res_aqi)
    predict_aqi.index = pd.date_range(date[0], date[1], freq="D")
    predict_pm2_5 = pd.Series(res_pm2_5)
    predict_pm2_5.index = pd.date_range(date[0], date[1], freq="D")
    # print(predict_aqi)
    # print(predict_pm2_5)
    # rms_aqi = math.sqrt(mean_squared_error(df.aqi[2215:], predict_aqi.values))
    # rms_pm2_5 = math.sqrt(mean_squared_error(df.pm2_5[2215:], predict_pm2_5.values))
    # print("aqi rms:",rms_aqi,"\n","pm2.5 rms:",rms_pm2_5)                                                 # 计算拟合度
    # ret = pd.DataFrame(list(zip(predict_aqi, predict_pm2_5)), columns=["aqi","pm2.5"])                    # 拼接为DataFrame



    return([predict_aqi.index.strftime('%Y-%m-%d').tolist(), predict_aqi.values.round(decimals=2).tolist(), predict_pm2_5.values.round(decimals=2).tolist()] )                                  # [[aqi],[pm2.5]])

if __name__ == "__main__":
    # citys = ['北京', '天津', '上海', '重庆', '石家庄', '太原', '西安',
    #          '济南', '长春', '哈尔滨', '南京', '杭州', '合肥', '南昌',
    #          '福州', '武汉', '长沙', '成都', '贵阳', '昆明', '广州', "郑州", "沈阳",
    #          '海口', '兰州', '西宁', '呼和浩特', '乌鲁木齐', '拉萨', '南宁', '银川']
    # data = []
    # today = (datetime.date.today() - timedelta(days=1)).strftime("%Y%m%d")
    # offset_day = date_offset(today)
    # for city in citys:
    #     city_data = predict_air(city, offset_day)
    #     print(city,":")
    #     print("predict_date:{}".format(city_data[0]))
    #     print("predict_AQI:{}".format(city_data[1]))
    #     print("predict_PM2.5:{}".format(city_data[2]))
    #     data.extend([[city, city_data[0][i], str(city_data[1][i]), str(city_data[2][i])] for i in range(len(city_data[0]))])
    # print(data)
    # save_to_mysql(data)

    predict_aqi()