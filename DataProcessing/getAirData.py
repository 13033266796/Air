from selenium import webdriver
import time
import pandas as pd
from urllib import parse
from lxml import etree

# citys = ['北京','天津','上海','重庆','石家庄','太原','西安','济南',
#         '沈阳' ,'长春','哈尔滨','南京','杭州','合肥','郑州',
#         '南昌', '福州','武汉','长沙' ,'成都','贵阳','昆明',
#         '广州','海口' ,'兰州' ,'西宁' ,'呼和浩特',
#         '乌鲁木齐', '拉萨','南宁','银川']



citys = ['南昌','郑州']# '福州' 2018-10

# print(len(a))

# times = pd.date_range("2013-12",datetime.datetime.now(), freq="m")
times = pd.date_range("2020-01","2020-03", freq="m")
# print(times)
times = times.map(lambda x: x.strftime('%Y-%m')).tolist()
# print(times.map(lambda x: x.strftime('%Y-%m')).tolist())



# urls = []
browser =webdriver.PhantomJS()
for city in citys:
    for date in times:
        url = 'https://www.aqistudy.cn/historydata/daydata.php?' + parse.urlencode({"city":city,"month":date})
        browser.get(url)
        time.sleep(3)

        get_html = browser.page_source
        # print(get_html)
        tree = etree.HTML(get_html)
        res = tree.xpath("//table/tbody/tr")
        # print(res)
        for i in res:
            tmp = i.xpath(".//td/text()")
            # print(tmp)
            if tmp:
                tmp.insert(0, city)
                print(tmp)
                with open(r"../Province_data/original/history_data_202001_202002.txt", "a", encoding="utf-8") as f:
                    f.write(",".join(tmp) + "\n")
        print("完成%s%s数据的爬取"%(city, date))


# url = 'https://www.aqistudy.cn/historydata/daydata.php?' + parse.urlencode({"city": "昆明", "month": date})
#
# browser =webdriver.PhantomJS()

# for date in times:
#     print(date)
#     url = 'https://www.aqistudy.cn/historydata/daydata.php?' + parse.urlencode({"city": "广州", "month": "201901"})
#     browser.get(url)
#     time.sleep(3)
#
#     get_html = browser.page_source
#     tree = etree.HTML(get_html)
#     res = tree.xpath("//table/tbody/tr")
#     for i in res:
#         tmp = i.xpath(".//td/text()")
#         if tmp :
#             tmp.insert(0, "广州")
#             print(tmp)
#             with open(r"../Province_data/original/history_data_add广州.txt", "a", encoding="utf-8") as f:
#                 f.write(",".join(tmp)+"\n")


