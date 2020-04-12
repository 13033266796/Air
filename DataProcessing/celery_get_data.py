# -*- coding:utf-8 -*-
import requests
import datetime
from datetime import timedelta
import json
import re
from selenium import webdriver
import time
import pandas as pd
from urllib import parse
from lxml import etree
from dateutil.relativedelta import relativedelta

CITY_MAPPING = {"沈阳": "shenyang", "西安": "xian", "哈尔滨": "haerbin", "长春": "changchun",
                "北京": "beijing", "天津": "tianjin", "石家庄": "shijiazhuang", "济南": "jinan",
                "呼和浩特": "huhehaote", "太原": "taiyuan", "郑州": "zhengzhou", "南京": "nanjing",
                "合肥": "hefei", "武汉": "wuhan", "上海": "shanghai", "杭州": "hangzhou", "南昌": "nanchang",
                "长沙": "changsha", "福州": "fuzhou", "广州": "guangzhou", "海口": "haikou", "南宁": "nanning",
                "昆明": "kunming", "贵阳": "guiyang", "重庆": "chongqing", "成都": "chengdu", "银川": "yinchuan",
                "西宁": "xining", "兰州": "lanzhou", "乌鲁木齐": "wulumuqi", "拉萨": "lasa", }

CITYS = ['北京', '天津', '上海', '重庆', '石家庄', '太原', '西安', '济南',
         '沈阳', '长春', '哈尔滨', '南京', '杭州', '合肥', '郑州',
         '南昌', '福州', '武汉', '长沙', '成都', '贵阳', '昆明',
         '广州', '海口', '兰州', '西宁', '呼和浩特',
         '乌鲁木齐', '拉萨', '南宁', '银川']

url = "http://www.pm25x.com/city/{}.htm"


def get_dayily_data():
    data = {}
    for city in CITYS:
        ave_pm = 0
        count = 0
        html_source = requests.get(url.format(CITY_MAPPING[city])).text
        print(f"网页源码 --> {html_source}")
        city_today = re.findall(r"<tr>(.*?)</tr>", html_source)[1:]
        print(f"表单数据 -- >{city_today}")
        aqi = re.search(r"""<div class="aqivalue">(.*?)</div>""", html_source).group(1)
        print(aqi)
        # 获取到一个城市所有的 tr 标签
        for tr in city_today:
            today_pm2_5 = re.findall(r"<td>(.*?)</td>", tr)
            if today_pm2_5[2] != '--':
                count += 1
                ave_pm += float(today_pm2_5[2])
        ave_pm = (ave_pm/count)
        ave_pm = round(ave_pm, 2)

        data[city] = {"aqi":float(aqi), "pm2.5":ave_pm}
        print({"city":city, "aqi":float(aqi), "pm2.5":ave_pm})
    print("获取实时数据成功")
    return data


def get_yesterday_data():
    yesterday_data = []
    yesterday = datetime.datetime.today().date() - timedelta(days=1)
    month = yesterday.strftime("%Y%m%d")[:-2]
    browser = webdriver.PhantomJS()
    for city in CITYS:
        url = 'https://www.aqistudy.cn/historydata/daydata.php?' + parse.urlencode({"city": city, "month": month})
        browser.get(url)
        time.sleep(3)
        get_html = browser.page_source
        tree = etree.HTML(get_html)
        res = tree.xpath("//table/tbody/tr")[0]
        tmp = res.xpath("//td/text()")

        yesterday_data.append([city,tmp[-8], tmp[-7], tmp[-6]])

    print(yesterday_data)
    return yesterday_data

get_dayily_data()