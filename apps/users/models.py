#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/29 15:30
# @describe: 用户数据库模型

from tortoise import models, fields

class User(models.Model):
    """用户模型"""
    id = fields.IntField(pk=True, description="用户id", unique=True)
    username = fields.CharField(max_length=50, description="用户名")
    password = fields.CharField(max_length=128, description="密码")
    email = fields.CharField(max_length=50, description="邮箱")
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")
    is_delete = fields.BooleanField(default=False, description="是否删除")
    is_superuser = fields.BooleanField(default=False, description="是否是超级管理员")

    def __str__(self):
        return self.username

    class Meta:
        table = "user"
        table_description = "用户表"
