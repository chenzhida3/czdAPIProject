#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/30 11:42
# @describe:
from celery.schedules import crontab

import settings

task_serializer = 'json'
accept_content = ['json']
result_serializer = 'json'
broker_url = settings.CELERY_BROKER_URL  # 消息队列的连接URL
result_backend = settings.CELERY_RESULT_BACKEND  # 结果后端的连接URL
task_default_queue = 'default'  # 默认任务队列
timezone = settings.timezone
