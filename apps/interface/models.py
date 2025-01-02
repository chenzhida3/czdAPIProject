#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/6 11:08
# @describe: 接口管理、接口用例模型

from tortoise import models, fields

class InterfaceManager(models.Model):
    """接口管理"""
    CHOICES = {
        ('1', '项目接口'),
        ('2', '第三方接口')
    }
    id = fields.IntField(pk=True, description="接口id", unique=True)
    project = fields.ForeignKeyField("models.TestProject", description="所属项目")
    name = fields.CharField(max_length=50, description="接口名称")
    url = fields.CharField(max_length=200, description="接口地址")
    method = fields.CharField(max_length=50, description="请求方法")
    type = fields.CharField(max_length=50, description="接口类型", choices=CHOICES, default="1")
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")
    is_delete = fields.BooleanField(default=False, description="是否删除")

    def __str__(self):
        return self.name

    class Meta:
        table = "interface_manager"
        table_description = "接口管理"


setup_script = """# 前置脚本(python):
# global_tools:全局工具函数
# data:用例数据 
# env: 局部环境
# ENV: 全局环境
# db: 数据库操作对象
"""
teardown_script = """# 后置脚本(python):
# global_tools:全局工具函数
# data:用例数据 
# response:响应对象response 
# env: 局部环境
# ENV: 全局环境
# db: 数据库操作对象
"""

class InterfaceCase(models.Model):
    """接口用例模型"""
    id = fields.IntField(pk=True, description="接口id", unique=True)
    interface = fields.ForeignKeyField("models.InterfaceManager", description="所属接口", related_name="cases")
    title = fields.CharField(max_length=50, description="用例标题")
    headers = fields.JSONField(description="请求头", default=dict, null=True, blank=True)
    request = fields.JSONField(description="请求参数", default=dict, null=True, blank=True)
    file = fields.JSONField(description="文件参数", default=list, null=True, blank=True)
    setup_script = fields.TextField(description="前置脚本", default=setup_script, null=True, blank=True)
    teardown_script = fields.TextField(description="后置脚本", default=teardown_script, null=True, blank=True)
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")
    is_delete = fields.BooleanField(default=False, description="是否删除")

    def __str__(self):
        return self.title

    class Meta:
        table = "interface_case"
        table_description = "接口用例"