#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/2 14:33
# @describe:
import json
import os
import shutil
from datetime import datetime

from fastapi import APIRouter, Depends, UploadFile, File

import settings
from .models import TestProject, TestEnv, TestFiles
from .schemas import (ProjectAddSchema, ProjectUpdateSchema, ProjectQuerySchema,
                      EnvAddSchema, EnvUpdateSchema)
from core.tools import paginate
from core.auth import check_jwt_token

project_router = APIRouter(
    dependencies=[Depends(check_jwt_token)]
)


@project_router.get('/project/list', summary='项目列表')
async def list_projects(page: int = None, page_size: int = None):
    """项目列表"""
    queryset = TestProject.filter(is_delete=False).all()
    fields_to_return = ['id', 'name', 'leader', 'create_time']
    items = await paginate(queryset, fields_to_return, page, page_size)

    return {'code': 200, 'data': items, 'msg': 'ok'}


@project_router.get('/project/{id}/', summary='项目详情')
async def get_project(id: int):
    """获取项目详情"""
    fields_to_return = ['id', 'name', 'leader', 'create_time']
    res = await TestProject.get_or_none(id=id, is_delete=False).values(*fields_to_return)
    if res is None:
        return {'code': 400, 'msg': '项目不存在'}
    return {'code': 200, 'data': res, 'msg': 'ok'}


@project_router.post('/project/create', summary='添加项目')
async def create_project(project: ProjectAddSchema):
    """添加项目"""
    await TestProject.create(**project.dict())
    return {'code': 200, 'msg': 'ok'}


@project_router.post('/project/update', summary='更新项目')
async def update_project(project: ProjectUpdateSchema):
    """更新项目"""
    res = await TestProject.get_or_none(id=project.id, is_delete=False)
    if res is None:
        return {'code': 400, 'msg': '项目不存在'}
    update_data = {
        "name": project.name,
        "leader": project.leader,
        "update_time": datetime.utcnow()
    }
    await TestProject.filter(id=project.id).update(**update_data)
    return {'code': 200, 'msg': 'ok'}


@project_router.post('/project/delete', summary='删除项目')
async def delete_project(project: ProjectQuerySchema):
    """删除项目"""
    res = await TestProject.get_or_none(id=project.id, is_delete=False)
    if res is None:
        return {'code': 400, 'msg': '项目不存在'}
    await TestProject.filter(id=project.id, is_delete=False).update(is_delete=True, update_time=datetime.utcnow())
    return {'code': 200, 'msg': 'ok'}


@project_router.get('/env/list', summary='环境列表')
async def list_env(page: int = None, page_size: int = None):
    """环境列表"""
    queryset = TestEnv.filter(is_delete=False).all()
    fields_to_return = ['id', 'name', 'host', 'headers', 'db', 'global_variables', 'debug_global_variable',
                        'global_func', 'project_id']
    items = await paginate(queryset, fields_to_return, page, page_size)

    return {'code': 200, 'data': items, 'msg': 'ok'}


@project_router.post('/env/create', summary='添加环境')
async def create_env(env: EnvAddSchema):
    # 判断环境所属的项目是否存在
    project = await TestProject.get_or_none(id=env.project_id, is_delete=False)
    if project is None:
        return {'code': 400, 'msg': '项目不存在'}
    await TestEnv.create(**env.dict())
    return {'code': 200, 'msg': 'ok'}


@project_router.post('/env/update', summary='更新环境')
async def update_env(env: EnvUpdateSchema):
    # 判断环境是否存在
    res = await TestEnv.get_or_none(id=env.id, is_delete=False)
    if res is None:
        return {'code': 400, 'msg': '环境不存在'}
    # 判断项目不存在
    project = await TestProject.get_or_none(id=env.project_id, is_delete=False)
    if project is None:
        return {'code': 400, 'msg': '当前项目不存在环境'}
    update_data = {
        "name": env.name,
        "host": env.host,
        "headers": env.headers,
        "db": env.db,
        "global_variables": env.global_variables,
        "debug_global_variable": env.debug_global_variable,
        "global_func": env.global_func,
        "project_id": env.project_id,
        "update_time": datetime.utcnow()
    }
    await TestEnv.filter(id=env.id).update(**update_data)
    return {'code': 200, 'msg': 'ok', 'data': update_data}


@project_router.post('/env/delete', summary='删除环境')
async def delete_env(env: ProjectQuerySchema):
    """删除环境"""
    res = await TestEnv.get_or_none(id=env.id, is_delete=False)
    if res is None:
        return {'code': 400, 'msg': '环境不存在'}
    await TestEnv.filter(id=env.id, is_delete=False).update(is_delete=True, update_time=datetime.utcnow())
    return {'code': 200, 'msg': 'ok'}


# 获取当前项目下的所有环境
@project_router.get('/env/project/{project_id}/', summary='当前项目下的所有环境')
async def get_env_by_project(project_id: int):
    """获取当前项目下的所有环境"""
    fields_to_return = ['id', 'name', 'host', 'headers', 'db', 'global_variables', 'debug_global_variable',
                        'global_func']
    # 判断当前项目是否存在
    project = await TestProject.get_or_none(id=project_id, is_delete=False)
    if project is None:
        return {'code': 400, 'msg': '项目不存在'}
    # 根据当前项目id，获取所有环境
    envs = await TestEnv.filter(project_id=project_id, is_delete=False).values(*fields_to_return)
    return {'code': 200, 'data': envs, 'msg': 'ok'}


# 测试文件接口
@project_router.get('/files/list', summary='测试文件列表')
async def list_files(page: int = None, page_size: int = None):
    """测试文件列表"""
    queryset = TestFiles.filter(is_delete=False).all()
    fields_to_return = ['id', 'file', 'info']
    items = await paginate(queryset, fields_to_return, page, page_size)

    return {'code': 200, 'data': items, 'msg': 'ok'}


@project_router.post('/files/upload', summary='添加测试文件')
async def create_files(file: UploadFile = File(...)):
    """添加测试文件"""
    filename = file.filename
    size = file.size

    # 上传文件不能超过500k
    if size > 1024 * 500:
        return {'code': 400, 'msg': '文件大小不能超过500k'}
    # 上传的文件名不能重复
    if filename in os.listdir(settings.MEDIA_ROOT):
        return {'code': 400, 'msg': '文件名已存在'}
    if os.path.isfile(settings.MEDIA_ROOT / filename):
        return {'code': 400, 'msg': '文件名已存在'}
    # 保存文件到指定目录
    with open(settings.MEDIA_ROOT / filename, 'wb') as f:
        shutil.copyfileobj(file.file, f)

    files = await TestFiles.create(file=settings.MEDIA_ROOT / filename,
                                   info=json.dumps([filename, 'files/{}'.format(filename), file.content_type]))

    return {'code': 200, 'msg': 'ok', 'data': files}

@project_router.post('/files/delete/{file_id}', summary='删除测试文件')
async def delete_files(file_id: int):
    """删除测试文件"""
    file_obj = await TestFiles.get_or_none(id=file_id, is_delete=False)
    if file_obj is None:
        return {'code': 400, 'msg': '文件不存在'}
    if file_obj.info[0] in os.listdir(settings.MEDIA_ROOT):
        os.remove(file_obj.file)
    await TestFiles.filter(id=file_id, is_delete=False).update(is_delete=True, update_time=datetime.utcnow())
    return {'code': 200, 'msg': 'ok'}
