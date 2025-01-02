#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/30 11:09
# @describe:
from celery import Celery

celery_app = Celery(
    'czdApiProject',
    broker_connection_retry_on_startup=True)

# 加载配置
celery_app.config_from_object('apps.celery_config')
# 自动发现任务模块
celery_app.autodiscover_tasks(['apps.task'], force=True)
@celery_app.task
def work01():
    print('work01')

@celery_app.task
def work02():
    print('work02')