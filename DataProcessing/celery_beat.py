from celery import Celery
from celery.schedules import crontab
import logging
import air_log

app = Celery("celery_beat", broker="redis://127.0.0.1:6379/2",
             backend="redis://127.0.0.1:6379/2")
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
        'schedule': crontab(minute=5, hour="*/1"),
        # 或者这么写，每小时执行一次
        # "schedule": crontab(minute=0, hour="*/1")
        # 执行的函数需要的参数
    },
    'day': {
        'task': 'tasks.day',
        'schedule': crontab(minute=10, hour=5),
    }
}
app.conf.timezone = 'Asia/Shanghai'
logger = logging.getLogger("air")