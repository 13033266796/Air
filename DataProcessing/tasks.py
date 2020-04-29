# coding:utf-8
import datetime
from datetime import timedelta
import os
import sys

sys.path.append(os.getcwd())

from celery_beat import app
from model import MysqlModel, LatestAirInfo, PredictAirInfo, AirInfo
from celery_get_data import get_dayily_data, get_yesterday_data, \
                            CITYS, get_dayily_data_new
from order_time import date_offset
from predict_data import predict_air


@app.task
def hour():
    with open("./test_celery.txt", "a", encoding="utf-8") as f:
        f.write(str(datetime.datetime.now()) + "开始获取数据\n")
        # 获取数据
        # data = get_dayily_data_new()
        data = get_dayily_data()
        # 存储数据
        with MysqlModel() as mysql:
            # 删除旧数据
            mysql.query(LatestAirInfo).delete()
            # 添加新数据
            for city in CITYS:
                mysql.add(LatestAirInfo(city_name=city,
                                        city_date=datetime.datetime.today().date(),
                                        city_AQI=data[city]["aqi"],
                                        city_PM2_5=data[city]["pm2.5"]))
        f.write(str(datetime.datetime.now()) + "成功存储数据\n")



    t = str(datetime.datetime.now())
    return f"{t} success !"

@app.task
def day():
    with open("./test_celery.txt", "a", encoding="utf-8") as f:
        # 更新历史空气质量数据库
        yesterday_data = get_yesterday_data() # [[北京]，[天津],...]
        with MysqlModel() as msyql:
            for city in yesterday_data:
                msyql.add(AirInfo(city_name=city[0],
                                city_date=datetime.datetime.strptime(city[1],'%Y-%m-%d').date(),
                                city_AQI=city[2],
                                city_PM2_5=city[3]))

        f.write(str(datetime.datetime.now()) + "开始预测\n")
        # 预测
        result = [] # 预测集
        today = (datetime.date.today()-timedelta(days=1)).strftime("%Y%m%d")
        offset_day = date_offset(today)
        print(f"***预测时间：{offset_day}***")
        for city in CITYS:
            city_data = predict_air(city, offset_day)
            result.extend(
                [[city, city_data[0][i], str(city_data[1][i]), str(city_data[2][i])] for i in range(len(city_data[0]))])
        f.write(str(datetime.datetime.now()) + "预测完成，开始存储数据\n")
        # 存储
        with MysqlModel() as mysql:
            mysql.query(PredictAirInfo).delete()
            for i in result:
                mysql.add(PredictAirInfo(city_name=i[0],
                                        city_date=datetime.datetime.strptime(i[1],'%Y-%m-%d').date(),
                                        city_AQI=i[2],
                                        city_PM2_5=i[3]))
        f.write(str(datetime.datetime.now()) + "完成预测数据存储\n")

    t = str(datetime.datetime.now())
    return f"{t} predict success !"




if __name__ =="__main__":
    day()
