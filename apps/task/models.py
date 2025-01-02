#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/10 11:36
# @describe:

from tortoise import models, fields


class TestTask(models.Model):
    """测试任务的模型类"""
    id = fields.IntField(pk=True, description="任务id", unique=True)
    name = fields.CharField(max_length=50, description="任务名称")
    project = fields.ForeignKeyField("models.TestProject", description="所属项目")
    scenes = fields.ManyToManyField("models.TestScene", related_name="tasks", description="关联业务流")
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")
    is_delete = fields.BooleanField(default=False, description="是否删除")

    def __str__(self):
        return self.name

    class Meta:
        table = "test_task"
        table_description = "测试任务"


class TestRecord(models.Model):
    """运行记录表模型"""
    id = fields.IntField(pk=True, description="记录id", unique=True)
    task = fields.ForeignKeyField("models.TestTask", description="关联任务")
    all = fields.IntField(description="总用例数", default=0)
    success = fields.IntField(description="成功用例数", default=0)
    fail = fields.IntField(description="失败用例数", default=0)
    error = fields.IntField(description="错误用例数", default=0)
    pass_rate = fields.FloatField(description="通过率", default='0')
    tester = fields.CharField(max_length=50, description="执行人")
    env = fields.ForeignKeyField("models.TestEnv", description="关联环境")
    statues = fields.CharField(max_length=50, description="运行状态")
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    is_delete = fields.BooleanField(default=False, description="是否删除")

    def __str__(self):
        return self.task.name

    class Meta:
        table = "test_record"
        table_description = "运行记录"

class TestReport(models.Model):
    """测试报告表模型"""
    id = fields.IntField(pk=True, description="报告id", unique=True)
    info = fields.JSONField(description="报告信息")
    record = fields.OneToOneField("models.TestRecord", description="关联测试记录")
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    is_delete = fields.BooleanField(default=False, description="是否删除")

    def __str__(self):
        return self.record.task.name

    class Meta:
        table = "test_report"
        table_description = "测试报告"
