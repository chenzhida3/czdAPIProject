#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/9 14:23
# @describe: 业务流模型

from tortoise import models, fields


class TestScene(models.Model):
    """业务流模型"""
    id = fields.IntField(pk=True, description="业务流id", unique=True)
    name = fields.CharField(max_length=50, description="业务流名称")
    project = fields.ForeignKeyField("models.TestProject", description="所属项目")
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")
    is_delete = fields.BooleanField(default=False, description="是否删除")

    def __str__(self):
        return self.name

    class Meta:
        table = "test_scenes"
        table_description = "业务流表"


class SceneToCase(models.Model):
    """业务流和接口用例中间表"""
    id = fields.IntField(pk=True, description="业务流id", unique=True)
    icase = fields.ForeignKeyField("models.InterfaceCase", description="接口用例", related_name="cases")
    scene = fields.ForeignKeyField("models.TestScene", description="业务流", related_name="scenes")
    sort = fields.IntField(description="排序", null=True, blank=True)
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")
    is_delete = fields.BooleanField(default=False, description="是否删除")

    def __str__(self):
        return self.icase.title

    class Meta:
        table = "scene_to_case"
        table_description = "业务流和接口用例中间表"
