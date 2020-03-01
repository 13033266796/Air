from example.geo_example import Faker
from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.globals import ChartType, SymbolType, ThemeType

a = ["aqi",12,"pm",43]

def geo_base() -> Geo:
    citys = ['北京', '天津', '上海', '重庆', '石家庄', '太原', '西安',
             '济南', '长春', '哈尔滨', '南京', '杭州', '合肥', '南昌',
             '福州', '武汉', '长沙', '成都', '贵阳', '昆明','广州',"郑州","沈阳",
             '海口', '兰州', '西宁', '呼和浩特','乌鲁木齐', '拉萨', '南宁', '银川']
    a_list = [(citys[i],[i,i*2])for i in range(len(citys))]
    # print(a_list)
    c = (
        Geo(init_opts=opts.InitOpts(theme=ThemeType.WESTEROS))# 地图主题
        .add_schema(maptype="china", is_roam=False, itemstyle_opts=opts.ItemStyleOpts(area_color = '#E6E6FA'))# 地图颜色
        # .add("geo", [list(z) for z in zip(Faker.provinces, Faker.values())])
        # .add("geo",[('南昌',12), ('北京',12), ('天津',12), ('拉萨',12), ('呼和浩特',12), ('桂林',12),('沈阳',12), ('乌鲁木齐',12),('海口',12)], type_="effectScatter",
        #      itemstyle_opts=opts.ItemStyleOpts(border_color = '#8A2BE2')) # 点的颜色
        .add("geo",a_list, type_="effectScatter",tooltip_opts=opts.TooltipOpts(formatter="{b}:"))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(series_index=[0][0]),
            title_opts=opts.TitleOpts(title="Geo-基本示例"),


        )
    )
    return c

c = geo_base()
c.render()
