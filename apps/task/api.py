#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/10 11:36
# @describe:

from datetime import datetime

from fastapi import APIRouter, Depends, BackgroundTasks

from core.auth import check_jwt_token
from .models import TestTask, TestRecord, TestReport
from .schemas import TaskAddSchema, TaskUpdateSchema, RunTaskSchema
from ..project.models import TestProject, TestEnv
from ..scenes.models import TestScene
from ..users.schemas import UserInfoSchema
from .tasks import run_test_task

task_router = APIRouter(
    dependencies=[Depends(check_jwt_token)]
)


@task_router.post('/tasks/create', summary='创建测试任务')
async def create_task(task: TaskAddSchema):
    """创建测试任务"""
    project = await TestProject.get_or_none(id=task.project, is_delete=False)
    if project is None:
        return {'code': 400, 'msg': '项目不存在'}
    scenes = await TestScene.filter(id__in=task.scenes, is_delete=False)
    if len(scenes) != len(task.scenes):
        return {'code': 400, 'msg': '业务流不存在'}
    task = await TestTask.create(name=task.name, project=project)
    await task.scenes.add(*scenes)
    result = {
        'id': task.id,
        'name': task.name,
        'project': task.project.id,
        'scenes': [i.id for i in scenes]
    }
    return {'code': 200, 'msg': '创建成功', 'data': result}


@task_router.post('/tasks/delete/{task_id}', summary='删除测试任务')
async def delete_task(task_id: int):
    """删除测试任务"""
    task = await TestTask.get_or_none(id=task_id, is_delete=False)
    if task is None:
        return {'code': 400, 'msg': '任务不存在'}
    await TestTask.filter(id=task_id).update(is_delete=True, update_time=datetime.utcnow())
    return {'code': 200, 'msg': 'ok'}


@task_router.post('/tasks/update', summary='修改测试任务')
async def update_task(task: TaskUpdateSchema):
    """修改测试任务"""
    "未完成"
    task_obj = await TestTask.get_or_none(id=task.id, is_delete=False)
    if task_obj is None:
        return {'code': 400, 'msg': '任务不存在'}
    project_obj = await TestProject.get_or_none(id=task.project, is_delete=False)
    if project_obj is None:
        return {'code': 400, 'msg': '项目不存在'}
    scenes = await TestScene.filter(id__in=task.scenes, is_delete=False)
    if len(scenes) != len(task.scenes):
        return {'code': 400, 'msg': '业务流不存在'}
    await task_obj.scenes.clear()
    await task_obj.scenes.add(*scenes)
    result = {
        'id': task.id,
        'name': task.name,
        'project': task.project,
        'scenes': [i.id for i in scenes],
        'update_time': datetime.utcnow()
    }
    await TestTask.filter(id=task.id).update(name=task.name, project_id=task.project, update_time=datetime.utcnow())
    return {'code': 200, 'msg': 'ok', "data": result}


@task_router.get('/tasks/', summary='获取测试任务列表')
async def get_task_list(project: int = None):
    """获取测试任务列表"""
    if project is None:
        tasks = await TestTask.filter(is_delete=False).all()
    else:
        tasks = await TestTask.filter(project_id=project, is_delete=False).all()

    result = []
    for task in tasks:
        result.append({
            'id': task.id,
            'name': task.name,
            'project': await TestProject.get_or_none(id=task.project_id).values('id', 'name'),
            'scenes': await task.scenes.all().values('id', 'name', 'project_id'),
            'create_time': task.create_time,
            'update_time': task.update_time
        })

    return {'code': 200, 'msg': 'ok', "data": result}


@task_router.get('/tasks/{task_id}', summary='获取单个测试任务详情')
async def get_task_detail(task_id: int):
    """获取单个测试任务详情"""
    task = await TestTask.get_or_none(id=task_id, is_delete=False)
    if task is None:
        return {'code': 400, 'msg': '任务不存在'}
    result = {
        'id': task.id,
        'name': task.name,
        'project': await TestProject.get_or_none(id=task.project_id).values('id', 'name'),
        'scenes': await task.scenes.all().values('id', 'name', 'project_id'),
        'create_time': task.create_time,
        'update_time': task.update_time
    }
    return {'code': 200, 'msg': 'ok', "data": result}


@task_router.get('/tasks/run/record', summary='获取运行记录')
async def get_tasks_record(task: int | None = None, project: int | None = None):
    """获取运行记录"""
    if task:
        records = await TestRecord.filter(task_id=task, is_delete=False).all()
    elif project:
        records = await TestRecord.filter(task__project_id=project, is_delete=False).all()
    else:
        records = await TestRecord.filter(is_delete=False).all()

    return {'code': 200, 'msg': 'ok', "data": records}


@task_router.get('/tasks/report/{record_id}', summary='获取报告')
async def get_report(record_id: int):
    """获取报告"""
    record = await TestRecord.get_or_none(id=record_id, is_delete=False)
    if record is None:
        return {'code': 400, 'msg': '记录不存在'}
    report = await TestReport.get_or_none(record_id=record.id, is_delete=False)
    if report is None:
        return {'code': 400, 'msg': '报告不存在'}

    return report.info


@task_router.post('/tasks/run', summary='运行测试任务')
async def run_task(task: RunTaskSchema, background_tasks: BackgroundTasks, user: UserInfoSchema = Depends(check_jwt_token)):
    """运行测试任务"""
    tester = user.get('username')
    env_id = task.env
    task_id = task.task
    background_tasks.add_task(run_test_task, env_id, task_id, tester)
    return {'code': 200, 'msg': '运行成功，稍后请查看测试报告'}

