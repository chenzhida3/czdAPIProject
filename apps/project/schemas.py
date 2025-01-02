#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/2 14:34
# @describe:

from fastapi import Body
from pydantic import BaseModel
from typing import Optional

class ProjectQuerySchema(BaseModel):
    """查询项目模型"""
    id: int
class ProjectAddSchema(BaseModel):
    """添加项目模型"""
    name: str
    leader: str

class ProjectUpdateSchema(ProjectQuerySchema, ProjectAddSchema):
    """更新项目模型"""
    pass


class EnvQuerySchema(BaseModel):
    """查询项目模型"""
    id: int


class EnvAddSchema(BaseModel):
    """添加环境模型"""
    name: str
    host: str
    headers: Optional[dict] = None
    db: Optional[dict] = None
    global_variables: Optional[dict] = None
    debug_global_variable: Optional[dict] = None
    global_func: Optional[dict] = None
    project_id: int

class EnvUpdateSchema(EnvQuerySchema, EnvAddSchema):
    """更新环境模型"""
    pass

