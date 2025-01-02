#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/2 14:34
# @describe:

from tortoise import models, fields



class TestProject(models.Model):
    """项目表"""
    id = fields.IntField(pk=True, description="项目id", unique=True)
    name = fields.CharField(max_length=50, description="项目名称")
    leader = fields.CharField(max_length=20, description="负责人")
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")
    is_delete = fields.BooleanField(default=False, description="是否删除")

    def __str__(self):
        return self.name

    class Meta:
        table = "test_project"
        table_description = "项目表"


class TestEnv(models.Model):
    """环境表"""
    id = fields.IntField(pk=True, description="环境id", unique=True)
    project = fields.ForeignKeyField("models.TestProject", related_name="所属项目")
    global_variables = fields.JSONField(description="全局变量", null=True, default=dict, blank=True)
    debug_global_variable = fields.JSONField(description="调试模式全局变量", default=dict, null=True, blank=True)
    db = fields.JSONField(description="数据库配置", default=list, null=True, blank=True)
    headers = fields.JSONField(description="全局请求头", default=dict, null=True, blank=True)
    global_func = fields.TextField(description="全局工具函数", default='', null=True, blank=True)
    name = fields.CharField(description="测试环境名称", max_length=50)
    host = fields.CharField(description="测试环境的host地址", max_length=50)
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")
    is_delete = fields.BooleanField(default=False, description="是否删除")

    def __str__(self):
        return self.name

    class Meta:
        table = "test_env"
        table_description = "环境表"

class TestFiles(models.Model):
    """测试文件表"""
    id = fields.IntField(pk=True, description="文件id", unique=True)
    file = fields.CharField(max_length=100, description="文件路径")
    info = fields.JSONField(description="文件信息", default=list, null=True, blank=True)
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")
    is_delete = fields.BooleanField(default=False, description="是否删除")

    def __str__(self):
        return self.info

    class Meta:
        table = "test_file"
        table_description = "测试文件表"
