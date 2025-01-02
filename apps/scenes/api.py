#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/9 14:23
# @describe:
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, BackgroundTasks
from core.auth import check_jwt_token
from core.tools import paginate

from .models import TestScene, SceneToCase
from .schemas import (SceneAddSchema, SceneUpdateSchema, SceneToCaseAddSchema, SceneToCaseUpdateSchema,
                      SortSchema, RunSceneSchema)
from .tasks import run_test_scene
from ..project.models import TestProject
from ..interface.models import InterfaceCase

scenes_router = APIRouter(
    dependencies=[Depends(check_jwt_token)]
)


@scenes_router.post('/scenes/create', summary='创建业务流')
async def create_scene(scene: SceneAddSchema):
    """
    创建业务流
    """
    project_obj = await TestProject.get_or_none(id=scene.project, is_delete=False)
    if project_obj is None:
        return {'code': 400, 'msg': '项目不存在'}
    await TestScene.create(name=scene.name, project_id=scene.project)
    return {'code': 200, 'msg': 'ok'}


@scenes_router.post('/scenes/delete/{scene_id}', summary='删除业务流')
async def delete_scene(scene_id: int):
    """
    删除业务流
    """
    scene_obj = await TestScene.get_or_none(id=scene_id, is_delete=False)
    if scene_obj is None:
        return {'code': 400, 'msg': '业务流不存在'}
    await scene_obj.filter(id=scene_id, is_delete=False).update(is_delete=True, update_time=datetime.utcnow())
    return {'code': 200, 'msg': 'ok'}


@scenes_router.post('/scenes/update', summary='更新业务流')
async def update_scene(scene: SceneUpdateSchema):
    """
    更新业务流
    """
    scene_obj = await TestScene.get_or_none(id=scene.id, is_delete=False)
    if scene_obj is None:
        return {'code': 400, 'msg': '业务流不存在'}
    update_data = {
        "name": scene.name,
        "project_id": scene.project,
        "update_time": datetime.utcnow()
    }
    await scene_obj.filter(id=scene.id, is_delete=False).update(**update_data)
    return {'code': 200, 'msg': 'ok'}


@scenes_router.get('/scenes', summary='获取业务流列表')
async def list_scenes(page: int = None, page_size: int = None):
    """
    获取业务流列表
    """
    fields_to_return = ['id', 'name', 'project_id', 'create_time', 'update_time']
    queryset = TestScene.filter(is_delete=False).all()
    items = await paginate(queryset, fields_to_return, page, page_size)
    return {'code': 200, 'data': items, 'msg': 'ok'}


@scenes_router.post('/scene/step/create', summary='创建业务员流测试步骤')
async def create_scene_step(step: SceneToCaseAddSchema):
    """
    创建业务流测试步骤
    """
    icase = await InterfaceCase.get_or_none(id=step.icase, is_delete=False)
    if icase is None:
        return {'code': 400, 'msg': '接口用例不存在'}
    scene_obj = await TestScene.get_or_none(id=step.scene, is_delete=False)
    if scene_obj is None:
        return {'code': 400, 'msg': '业务流不存在'}
    await SceneToCase.create(icase_id=step.icase, scene_id=step.scene, sort=step.sort)
    return {'code': 200, 'msg': 'ok'}


@scenes_router.post('/scene/step/delete/{step_id}', summary='删除业务流测试步骤')
async def delete_scene_step(step_id: int):
    """
    删除业务流测试步骤
    """
    step_obj = await SceneToCase.get_or_none(id=step_id, is_delete=False)
    if step_obj is None:
        return {'code': 400, 'msg': '业务流测试步骤不存在'}
    await step_obj.filter(id=step_id, is_delete=False).update(is_delete=True, update_time=datetime.utcnow())
    return {'code': 200, 'msg': 'ok'}


@scenes_router.post('/scene/step/update', summary='更新业务员流测试步骤')
async def update_scene_step(step: SceneToCaseUpdateSchema):
    """
    更新业务流测试步骤
    """
    step_obj = await SceneToCase.get_or_none(id=step.id, is_delete=False)
    if step_obj is None:
        return {'code': 400, 'msg': '业务流测试步骤不存在'}
    update_data = {
        "icase_id": step.icase,
        "scene_id": step.scene,
        "sort": step.sort,
        "update_time": datetime.utcnow()
    }
    await step_obj.filter(id=step.id, is_delete=False).update(**update_data)
    return {'code': 200, 'msg': 'ok'}


@scenes_router.get('/scene/step', summary='获取业务流测试步骤列表')
async def list_scene_step(scene_id: int = None):
    """
    获取业务流测试步骤列表
    """
    if scene_id:
        step = await SceneToCase.filter(scene_id=scene_id,is_delete=False).all().order_by('sort')
    else:
        step = await SceneToCase.filter(is_delete=False).all().order_by('sort')
    step_all = []
    for s in step:
        data = {
            "id": s.id,
            "sort": s.sort,
            "icase": await InterfaceCase.filter(id=s.icase_id, is_delete=False).first().values('id', 'title'),
            "scene": s.scene_id,
            "create_time": s.create_time,
            "update_time": s.update_time
        }
        step_all.append(data)
    return {'code': 200, 'data': step_all, 'msg': 'ok'}


@scenes_router.post('/scene/step/order', summary='修改排序')
async def update_scene_step_order(items: List[SortSchema]):
    """
    修改排序
    """
    for item in items:
        await SceneToCase.filter(id=item.id, is_delete=False).update(sort=item.sort)
    return {'code': 200, 'msg': 'ok'}

@scenes_router.post('/scene/run', summary='运行业务流')
async def run_scene(scene: RunSceneSchema,background_tasks: BackgroundTasks):
    env_id = scene.env
    task_id = scene.scene
    background_tasks.add_task(run_test_scene, env_id, task_id)
    return {'code': 200, 'msg': '运行成功，稍后请查看测试报告'}