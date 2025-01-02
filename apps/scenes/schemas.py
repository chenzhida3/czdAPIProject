#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/9 14:23
# @describe:

from pydantic import BaseModel


class SceneAddSchema(BaseModel):
    """
    业务流添加
    """
    name: str
    project: int


class SceneUpdateSchema(SceneAddSchema):
    """业务流更新"""
    id: int


class SceneToCaseAddSchema(BaseModel):
    """
    业务流添加用例
    """
    scene: int
    icase: int
    sort: int


class SceneToCaseUpdateSchema(SceneToCaseAddSchema):
    """业务流更新用例"""
    id: int


class SortSchema(BaseModel):
    """执行顺序修改参数"""
    id: int
    sort: int

class RunSceneSchema(BaseModel):
    """业务流查询参数"""
    env: int
    scene: int
