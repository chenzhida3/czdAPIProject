#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/6 11:08
# @describe:
from pydantic import BaseModel
from typing import Dict

class InterfaceManageSchema(BaseModel):
    """添加接口管理模型"""
    name: str
    url: str
    method: str
    type: str
    project: int

class InterfaceManageQuerySchema(BaseModel):
    id: int

class InterfaceManageUpdateSchema(InterfaceManageQuerySchema, InterfaceManageSchema):
    pass


class CaseAddSchema(BaseModel):
    """添加用例模型"""
    interface: int
    title: str
    request: dict = {}
    file: list = []
    headers: dict = {}
    setup_script: str = '"# 前置脚本(python):\n# global_tools:全局工具函数\n# data:用例数据 \n# env: 局部环境\n# ENV: 全局环境\n# db: 数据库操作对象\n"'
    teardown_script: str = "# 后置脚本(python):\n# global_tools:全局工具函数\n# data:用例数据 \n# response:响应对象response \n# env: 局部环境\n# ENV: 全局环境\n# db: 数据库操作对象\n"

class CaseUpdateSchema(CaseAddSchema):
    """更新用例模型"""
    id: int

class RunCaseInterSchema(BaseModel):
    url: str
    method: str
    name: str


# 运行单条测试的数据
class CaseSchema(BaseModel):
    """运行测试模块"""
    title: str
    setup_script: str
    teardown_script: str
    headers: dict = {}
    request: dict = {}
    interface: RunCaseInterSchema

# class RunCaseSchema(BaseModel):
#     """运行测试模块"""
#     env: int
#     case: CaseSchema

class RunCaseSchema(BaseModel):
    """运行测试模块"""
    env: int
    case: int



