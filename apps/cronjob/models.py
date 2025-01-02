#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/27 16:24
# @describe: 定时任务

from tortoise import models, fields

class CronJob(models.Model):
    """
    定时任务
    """
    id = fields.IntField(pk=True, description="任务id", unique=True)
    project = fields.ForeignKeyField("models.TestProject", description="所属项目")
    env = fields.ForeignKeyField("models.TestEnv", description="关联环境")
    task = fields.ForeignKeyField("models.TestTask", description="执行任务")
    name = fields.CharField(max_length=50, description="任务名称")
    rule = fields.CharField(max_length=50, description="执行的规则")
    status = fields.BooleanField(description="状态", default=False)
    is_delete = fields.BooleanField(default=False, description="是否删除")
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    job_id = fields.CharField(max_length=50, null=True, description="任务id")

    def __str__(self):
        return self.name

    class Meta:
        table = "cron_job"
        table_description = "定时任务"