#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/27 16:29
# @describe:
from pydantic import BaseModel

class CronJobAddSchema(BaseModel):
    """添加定时任务模型"""
    project: int
    env: int
    task: int
    name: str
    rule: str
    status: bool

class CronJobDeleteSchema(BaseModel):
    """删除定时任务"""
    job_id: str

class CronJobChangeStatusSchema(CronJobDeleteSchema):
    """更改定时任务状态"""
    status: bool

class CronJobUpdateSchema(CronJobAddSchema):
    """更新定时任务"""
    id: int

