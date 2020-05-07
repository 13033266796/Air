/* 获取城市数据
* @method GetData
*@param{string}cityname 城市名
*/
function GetData(cityname){
	if(!$.trim(cityname)){
		alert('请先选择城市！')
	}
	
	// 根据城市名称异步获取该城市的历史数据
	$.ajax({
		/*url:'http://47.115.24.101:80/api/data/?',*/                
		url:'http://air.chanshin.cn/api/data/?',
		data:{city:cityname},
		type:'get',
		dataType:'json',
		success:function(res){
			// 显示折线图
			ShowLineChart(cityname, res.predict_date,res.predict_pm2_5,res.predict_aqi);
			// 显示柱状图
			ShowHistogramChart(cityname,res.months,res.data_AQI,res.data_PM2_5);
		},
		error:function(xhr, textStatus, errorThrown){
			/*错误信息处理*/
　　　　　　alert('发生(' + xhr.status + ')错误：' +xhr.statusText);
		}
	});
	
}

/* 显示柱状图
* @method ShowLineChart
*@param{string}cityname 城市名称
*@param{array}MonthArray 月份数组
*@param{array}AQIArray AQI数组
*@param{array}PM2_5Array PM2.5数组
*/
function ShowHistogramChart(cityname,MonthArray,AQIArray,PM2_5Array){
	
	// 在这里组装Options的数据
	var optionArray = [];
	if(MonthArray.length > 0){
		for(i = 0,len = MonthArray.length; i < len; i++) {
			var item = {};
			item.title = {};
			item.title.text = cityname + '历史空气质量';
			
			item.series = [];
			var aqiItem = {}
			aqiItem.data = AQIArray[MonthArray[i]];
			item.series.push(aqiItem); // 将aqi插入series
			var pmItem = {}
			pmItem.data = PM2_5Array[MonthArray[i]];
			item.series.push(pmItem); // 将pm2.5插入series
			
			//console.log(item); // 调试打印Item对象
			optionArray.push(item); //将Item插入Options
		}
		
	}
	
	//console.log(optionArray)// 调试打印optionArray对象
	
	// 基于准备好的dom，初始化echarts实例
	var myChart = echarts.init(document.getElementById('LineChart'));

	// 指定图表的配置项和数据
	var dataMap = {};

	// 数据源
	dataMap.dataAQI = AQIArray;
	dataMap.dataPM2_5 = PM2_5Array;

	option_1 = {
		baseOption: {
			timeline: {
				axisType: 'category',
				autoPlay: true,
				playInterval: 1000,
				data: MonthArray
				,
				label: {
					formatter: function (s) {
						// return (new Date(s)).getFullYear();
						return (new Date(s)).getFullYear()
					}
				}
			},
			title: {
				subtext: '数据来自Jasper'
			},
			tooltip: {
			},
			legend: {
				left: 'right',
				// data: ['第一产业', '第二产业', '第三产业', 'GDP', '金融', '房地产'],
				data: "GDP",
				selected: {
					// 'GDP': false, '金融': false, '房地产': false

				}
			},
			calculable: true,
			grid: {
				top: 80,
				bottom: 100,
				tooltip: {
					trigger: 'axis',
					axisPointer: {
						type: 'shadow',
						label: {
							show: true,
							formatter: function (params) {
								return params.value.replace('\n', '');
							}
						}
					}
				}
			},
			xAxis: [
				{
					'type': 'category',
					'axisLabel': { 'interval': 0 },
					'data': [
						'01', '02', '03', '04', '05', '06', '07', '08',
						'09', '10', '11', '12', '13', '14', '15', '16',
						'17', '18', '19', '20', '21', '22', '23', '24',
						'25', '26', '27', '28', '29', '30', '31'
					],
					splitLine: { show: false }
				}
			],
			yAxis: [
				{
					type: 'value',
					name: 'AQI/PM2.5',
					'axisLabel': { 'interval': 0 },
				}
			],
			series: [
				{ name: 'AQI', type: 'bar' },
				{ name: 'PM2.5', type: 'bar' },
			]
		},
		options: optionArray
	};
	// 使用刚指定的配置项和数据显示图表。
	myChart.setOption(option_1);
}

/* 显示折线图
* @method ShowLineChart
*@param{array}predict_date 日期数组
*@param{array}predict_pm2_5 PM2.5数组
*@param{array}predict_aqi AQI数组
*/
function ShowLineChart(cityname, predict_date,predict_pm2_5,predict_aqi){

        var lineChart = echarts.init(document.getElementById('BarChart'));

        option = {
            title: {
                text: cityname + '近七日空气质量趋势'
            },
            tooltip: {
                trigger: 'axis'
            },
            legend: {
                // data: ['邮件营销', '联盟广告', '视频广告', '直接访问', '搜索引擎']
                data: ['PM2.5', 'AQI']
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            toolbox: {
                feature: {
                    saveAsImage: {}
                }
            },
            xAxis: {
                type: 'category',
                boundaryGap: true,
                // data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
                data: predict_date
            },
            yAxis: {
                type: 'value'
            },
            series: [

                {
                    name: 'PM2.5',
                    type: 'line',
                    // stack: '总量',
                    data: predict_pm2_5
                },
                {
                    name: 'AQI',
                    type: 'line',
                    // stack: '总量',
                    // data: [120, 132, 101, 134, 90, 230, 210]
                    data: predict_aqi
                },

            ],
            backgroundColor: '',
        };
        lineChart.setOption(option);
}
