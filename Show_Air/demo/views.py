from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from display_app.models import AirInfo,PredictInfo
import pandas as pd


def index(request):
    # 首页默认展示北京的空气质量数据
    cur = AirInfo.objects.filter(city_name="北京")

    # 从数据库获取北京历史空气质量数据
    history_data = {data.city_date.strftime('%Y-%m-%d'): [data.city_AQI, data.city_PM2_5] for data in cur}

    # 预测数据
    cur_predict = PredictInfo.objects.filter(city_name="北京")
    predict_date = [date.city_date.strftime('%Y-%m-%d') for date in cur_predict]
    predict_aqi = [float(aqi.city_AQI) for aqi in cur_predict]
    predict_pm2_5 = [float(pm2_5.city_PM2_5) for pm2_5 in cur_predict]

    # 今日数据
    cur_today = AirInfo.objects.filter(city_date = '2019-12-31')
    citys = ['北京', '天津', '上海', '重庆', '石家庄', '太原', '西安',
             '济南', '长春', '哈尔滨', '南京', '杭州', '合肥', '南昌',
             '福州', '武汉', '长沙', '成都', '贵阳', '昆明', '广州', "郑州", "沈阳",
             '海口', '兰州', '西宁', '呼和浩特', '乌鲁木齐', '拉萨', '南宁', '银川']
    today_aqi = []
    today_pm2_5 = []
    for city in citys:
        for data in cur_today:
            if data.city_name == city:
                today_aqi.append(float(data.city_AQI))
                today_pm2_5.append(float(data.city_PM2_5))

    # 生成日期 --月份
    dates = pd.date_range("2013-12", "2020-01", freq="m")
    months = dates.map(lambda x: x.strftime('%Y-%m')).tolist()  # [2013-12 2014-01 2014-02 ... 2019-31]
    # 生成日期 --日
    days = [str(day).rjust(2, '0') for day in range(1, 32)]  # [01 02 03 04 ... 31 ]
    # 格式化数据
    format_data_AQI = {}
    format_data_PM2_5 = {}

    for month in months:
        AQI = []
        PM2_5 = []
        for day in days:
            if month + "-" + day in history_data.keys():  # 真实存在的日期
                AQI.append(float(history_data[month + "-" + day][0]))
                PM2_5.append(float(history_data[month + "-" + day][1]))
            else:  # 不存在的日期 如：2.30, 4.31, 6.31...等等
                AQI.append(0)
                PM2_5.append(0)
        format_data_AQI[month] = AQI
        format_data_PM2_5[month] = PM2_5

    return render(request, "demo/demo.html", context={"data_AQI": format_data_AQI,
                                                      "data_PM2_5": format_data_PM2_5,
                                                      "city": "北京", "months": months,
                                                      "predict_date":predict_date,
                                                      "predict_aqi":predict_aqi,
                                                      "predict_pm2_5":predict_pm2_5,
                                                      "today_aqi":today_aqi,
                                                      "today_pm2_5":today_pm2_5})


def get_city_history_data(request):
    city_url = request.GET["city"]
    cur = AirInfo.objects.filter(city_name=city_url)

    # 从数据库获取北京历史空气质量数据
    history_data = {data.city_date.strftime('%Y-%m-%d'): [data.city_AQI, data.city_PM2_5] for data in cur}

    # 预测数据
    cur_predict = PredictInfo.objects.filter(city_name=city_url)
    predict_date = [date.city_date.strftime('%Y-%m-%d') for date in cur_predict]
    predict_aqi = [float(aqi.city_AQI) for aqi in cur_predict]
    predict_pm2_5 = [float(pm2_5.city_PM2_5) for pm2_5 in cur_predict]

    # 今日数据
    cur_today = AirInfo.objects.filter(city_date='2019-12-31')
    citys = ['北京', '天津', '上海', '重庆', '石家庄', '太原', '西安',
             '济南', '长春', '哈尔滨', '南京', '杭州', '合肥', '南昌',
             '福州', '武汉', '长沙', '成都', '贵阳', '昆明', '广州', "郑州", "沈阳",
             '海口', '兰州', '西宁', '呼和浩特', '乌鲁木齐', '拉萨', '南宁', '银川']
    today_aqi = []
    today_pm2_5 = []
    for city in citys:
        for data in cur_today:
            if data.city_name == city:
                today_aqi.append(float(data.city_AQI))
                today_pm2_5.append(float(data.city_PM2_5))

    # 生成日期 --月份
    dates = pd.date_range("2013-12", "2020-01", freq="m")
    months = dates.map(lambda x: x.strftime('%Y-%m')).tolist()  # [2013-12 2014-01 2014-02 ... 2019-31]
    # 生成日期 --日
    days = [str(day).rjust(2, '0') for day in range(1, 32)]  # [01 02 03 04 ... 31 ]
    # 格式化数据
    format_data_AQI = {}
    format_data_PM2_5 = {}

    for month in months:
        AQI = []
        PM2_5 = []
        for day in days:
            if month + "-" + day in history_data.keys():  # 真实存在的日期
                AQI.append(float(history_data[month + "-" + day][0]))
                PM2_5.append(float(history_data[month + "-" + day][1]))
            else:  # 不存在的日期 如：2.30, 4.31, 6.31...等等
                AQI.append(0)
                PM2_5.append(0)
        format_data_AQI[month] = AQI
        format_data_PM2_5[month] = PM2_5

    return render(request, "demo/demo.html", context={"data_AQI": format_data_AQI,
                                                      "data_PM2_5": format_data_PM2_5,
                                                      "city": city_url, "months": months,
                                                      "predict_date": predict_date,
                                                      "predict_aqi": predict_aqi,
                                                      "predict_pm2_5": predict_pm2_5,
                                                      "today_aqi": today_aqi,
                                                      "today_pm2_5": today_pm2_5})

def predict(request):
    cur = PredictInfo.objects.filter(city_name="深圳")

    # 从数据库获取北京历史空气质量数据
    predict_data = {data.city_date.strftime('%Y-%m-%d'): [data.city_AQI, data.city_PM2_5] for data in cur}
    print(predict_data)
    return HttpResponse(predict_data)


def file_form(request):

    return HttpResponse("1")
