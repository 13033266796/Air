from celery import Celery
from celery.schedules import crontab
from datetime import timedelta
import datetime
from DataProcessing import celery_get_data

app = Celery("celery_beat", broker="redis://47.115.24.101:6379/2",
             backend="redis://47.115.24.101:6379/2")
# # test
# app = Celery("tasks", broker="redis://127.0.0.1:6379/6", backend="redis://127.0.0.1:6379/6")
# app.config_from_object("Config")
app.conf.beat_schedule = {
    'hour': {
        # 具体需要执行的函数
        # 该函数必须要使用@app.task装饰
        'task': 'tasks.hour',
        # 定时时间
        # 每分钟执行一次，不能为小数
        'schedule': crontab(minute="*/1", hour="*"),
        # 或者这么写，每小时执行一次
        # "schedule": crontab(minute=0, hour="*/1")
        # 执行的函数需要的参数
    },
    'day':{
        'task': 'tasks.hour',
        'schedule': crontab(minute="*/1", hour="*"),
    }
}
app.conf.timezone = 'Asia/Shanghai'


@app.task
def todo():
    with open("./test_celery.txt", "a", encoding="utf-8") as f:
        f.write(str(datetime.datetime.now()) + "\n")
    return " todo 的返回值"
