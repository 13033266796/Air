import time
import datetime
# from datetime import datetime
from datetime import timedelta
from DataProcessing import predict_data

# 从今天起 往后推七天 日期
def date_offset(date_str, days_count=7):
    date_list = time.strptime(date_str, "%Y%m%d")
    y, m, d = date_list[:3]
    delta_start = timedelta(days=1)
    delta_end = timedelta(days=7)
    start = datetime.datetime(y, m, d) + delta_start
    end = datetime.datetime(y, m, d) + delta_end
    start = start.strftime("%Y%m%d")
    end = end.strftime("%Y%m%d")
    return [start, end]
# 今天
today = datetime.date.today().strftime("%Y%m%d")
# today= "20191231"
offset_day = date_offset(today)

print(offset_day)

citys = ['北京', '天津', '上海', '重庆', '石家庄', '太原', '西安',
             '济南', '长春', '哈尔滨', '南京', '杭州', '合肥', '南昌',
             '福州', '武汉', '长沙', '成都', '贵阳', '昆明', '广州', "郑州", "沈阳",
             '海口', '兰州', '西宁', '呼和浩特', '乌鲁木齐', '拉萨', '南宁', '银川']
data = []
for city in citys:
    city_data = predict_data.predict_air(city, offset_day)
    data.extend([[city, city_data[0][i], str(city_data[1][i]), str(city_data[2][i])] for i in range(len(city_data[0]))])
print(data)