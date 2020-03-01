import numpy as np
import pandas as pd
import pymysql
from sqlalchemy import create_engine

def select_none_data():
    conn = pymysql.connect(host='34.92.92.176', port=3306, user='root', passwd='123456', db='show_air',
                           charset='utf8')
    cursor1 = conn.cursor()
    citys = ['北京', '天津', '上海', '重庆', '石家庄', '太原', '西安',
             '济南', '长春', '哈尔滨', '南京', '杭州', '合肥', '南昌',
             '福州', '武汉', '长沙', '成都', '贵阳', '昆明','广州',"郑州","沈阳",
             '海口', '兰州', '西宁', '呼和浩特','乌鲁木齐', '拉萨', '南宁', '银川']
    for city in citys:
        # sql = '''SELECT a.city_date ,count(*) as count from                                  # 查询一个城市中的缺失值
        #         (SELECT city_date FROM display_app_airinfo WHERE city_name="郑州"
        #         UNION ALL
        #         SELECT city_date FROM display_app_airinfo WHERE city_name="%s") as a
        #         GROUP BY a.city_date
        #         HAVING count = 1
        #         '''%(city)
        sql = '''
              SELECT a.city_date ,count(*) as count FROM
            (SELECT city_date FROM display_app_airinfo WHERE city_name="%s") as a
            GROUP BY a.city_date
            HAVING count >1
              '''%(city)                                                                        # 查一个城市信息中是否含有重复值
        cursor1.execute(sql)
        ret = cursor1.fetchall()# 元组 ((datetime.date(2013, 12, 1), 1), (datetime.date(2016, 4, 16), 1))
        print(ret)
        # for line in ret:
        #     with open("../Province_data/original/data_preprocessing.txt","a",encoding="utf-8") as f:
        #         f.write(city+","+line[0].strftime("%Y-%m-%d")+",0.00,0.00\n")


select_none_data()