import sys
import os
sys.path.append(os.getcwd())
import logging.config

root_dir = os.path.dirname(__name__)
DEBUG = True
# ==============================================================================
# 日志配置
# ==============================================================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s-%(asctime)s: %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'air': {
            'level': 'DEBUG' if DEBUG else 'INFO',  # 日志级别： debug, error, warning, info
            'class': 'logging.FileHandler',  # 日志输出类型
            # 日志输出文件 os.getcwd()获取当前运行文件所在目录
            'filename': os.path.join(root_dir, "air.log"),
            'formatter': 'verbose'  # 日志排版
        }
    },
    'loggers': {
        'air': {
            'handlers': ['air'],
            'level': 'DEBUG' if DEBUG else 'INFO',  # 日志级别： debug, error, warning, info
            'propagate': True,
        }
    }
}

logging.config.dictConfig(LOGGING)