#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/29 15:49
# @describe:
import os
from pathlib import Path

# 获取当前项目的基础路径
BASE_DIR = Path(__file__).resolve().parent

# 数据库配置
DATABASE = {
    'host': 'localhost',
    'port': '3306',
    'user': 'root',
    'password': '123456',
    'database': 'apiproject',
}
# redis配置
REDIS = {
    'host': 'localhost',
    'port': '6379',
    'db': '8',
    'password': None,
}

# app中的models
APP_MODELS = [
    'apps.users.models',
    'apps.project.models',
    'apps.interface.models',
    'apps.scenes.models',
    'apps.task.models',
    'apps.cronjob.models'
]

# TORTOISE_ORM配置
TORTOISE_ORM = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.mysql',
            'credentials': DATABASE
        },
    },
    'apps': {
        'models': {
            'models': ['aerich.models', *APP_MODELS],
            'default_connection': 'default',
        },

    }
}

# JWTToken鉴权配置
# token秘钥
SECRET_KEY = 'eac77e4e9a9a767b72345432qasdf31bec56714607f617a3fbdfbd53'
# token加密算法
ALGORITHM = "HS256"
# token过期时间(天)
ACCESS_TOKEN_EXPIRE_MINUTES = 24*60


# 文件上传的路径
MEDIA_ROOT = BASE_DIR / 'files'


# celery配置
CELERY_BROKER_URL = 'redis://localhost:6379/9'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/10'
timezone = 'Asia/Shanghai'

