#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/10 11:36
# @describe:
from pydantic import BaseModel
from typing import Union

class TaskAddSchema(BaseModel):
    """添加测试任务模型"""
    name: str
    project: int
    scenes: list

class TaskUpdateSchema(TaskAddSchema):
    id: int

class RunTaskSchema(BaseModel):
    """运行测试任务模型"""
    env: int
    task: int
