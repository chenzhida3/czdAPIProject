#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/6 11:08
# @describe:
import json
from datetime import datetime

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from core.auth import check_jwt_token
from core.tools import paginate
from .models import InterfaceManager, InterfaceCase
from .schemas import InterfaceManageSchema, InterfaceManageUpdateSchema, CaseAddSchema, CaseUpdateSchema, \
    RunCaseSchema
from ..project.models import TestProject, TestEnv
from czdApiTestEngine import testRunner

interface_router = APIRouter(
    dependencies=[Depends(check_jwt_token)]
)

"""获取接口管理列表"""


@interface_router.get('/manage/list', summary='接口管理列表')
async def list_manage_interfaces(project: int = None):
    # 定义要输出的字段
    if project is not None:
        interfaces = await InterfaceManager.filter(project_id=project, is_delete=False).prefetch_related('cases')
    else:
        interfaces = await InterfaceManager.filter(is_delete=False).prefetch_related('cases')
    interfaces_data = []
    for interface in interfaces:
        interface_data = {
            "id": interface.id,
            "project": interface.project_id,
            "name": interface.name,
            "url": interface.url,
            "method": interface.method,
            "type": interface.type,
            "cases": [
                {"id": case.id, "title": case.title}
                for case in interface.cases
            ]
        }
        interfaces_data.append(interface_data)
    return {'code': 200, 'msg': 'ok', 'data': interfaces_data}


"""添加接口管理"""


@interface_router.post('/manage/create', summary='添加接口管理')
async def create_manage_interface(interface: InterfaceManageSchema):
    project = await TestProject.get_or_none(id=interface.project, is_delete=False)
    if not project:
        return {'code': 400, 'msg': '项目不存在'}
    interface_data = {
        'name': interface.name,
        'method': interface.method,
        'url': interface.url,
        'type': interface.type,
        'project_id': interface.project
    }
    await InterfaceManager.create(**interface_data)
    return {'code': 200, 'msg': 'ok'}


"""更新接口管理"""


@interface_router.post('/manage/update', summary='更新接口管理')
async def update_manage_interface(interface: InterfaceManageUpdateSchema):
    interface_obj = await InterfaceManager.get_or_none(id=interface.id, is_delete=False)
    if not interface_obj:
        return {'code': 400, 'msg': '接口不存在'}
    project_onj = await TestProject.get_or_none(id=interface.project, is_delete=False)
    if not project_onj:
        return {'code': 400, 'msg': '项目不存在'}
    update_data = {
        'name': interface.name,
        'method': interface.method,
        'url': interface.url,
        'type': interface.type,
        'project_id': interface.project,
        'update_time': datetime.utcnow()
    }
    await InterfaceManager.filter(id=interface.id).update(**update_data)
    return {'code': 200, 'msg': 'ok'}


@interface_router.post('/manage/delete/{interface_id}', summary='删除接口管理')
async def delete_manage_interface(interface_id: int):
    """删除接口管理"""
    interface_obj = await InterfaceManager.get_or_none(id=interface_id, is_delete=False)
    if not interface_obj:
        return {'code': 400, 'msg': '接口不存在'}
    await InterfaceManager.filter(id=interface_id, is_delete=False).update(is_delete=True,
                                                                           update_time=datetime.utcnow())
    return {'code': 200, 'msg': 'ok'}


@interface_router.post('/cases/create', summary='添加用例')
async def create_interface_case(case: CaseAddSchema):
    """添加用例"""
    interface_obj = await InterfaceManager.get_or_none(id=case.interface, is_delete=False)
    if not interface_obj:
        return {'code': 400, 'msg': '接口不存在'}
    case_data = {
        'title': case.title,
        'interface_id': case.interface,
        'request': case.request,
        'headers': case.headers,
        'file': case.file,
        'setup_script': case.setup_script,
        'teardown_script': case.teardown_script
    }
    await InterfaceCase.create(**case_data)
    return {'code': 200, 'msg': 'ok'}


@interface_router.post('/cases/delete/{case_id}', summary='删除用例')
async def delete_interface_case(case_id: int):
    """删除用例"""
    case_obj = await InterfaceCase.get_or_none(id=case_id, is_delete=False)
    if not case_obj:
        return {'code': 400, 'msg': '用例不存在'}
    await InterfaceCase.filter(id=case_id, is_delete=False).update(is_delete=True, update_time=datetime.utcnow())
    return {'code': 200, 'msg': 'ok'}


@interface_router.post('/cases/update', summary='更新用例')
async def update_interface_case(case: CaseUpdateSchema) -> dict:
    """更新用例"""
    case_obj = await InterfaceCase.get_or_none(id=case.id, is_delete=False)
    if not case_obj:
        return {'code': 400, 'msg': '用例不存在'}
    update_data = {
        'title': case.title,
        'request': case.request,
        'headers': case.headers,
        'file': case.file,
        'setup_script': case.setup_script,
        'teardown_script': case.teardown_script,
        'update_time': datetime.utcnow(),
        'interface_id': case.interface
    }
    await InterfaceCase.filter(id=case.id).update(**update_data)
    return {'code': 200, 'msg': 'ok'}


@interface_router.get('/cases', summary='用例列表')
async def list_interface_cases(page: int = None, page_size: int = None) -> dict:
    """获取接口用例列表"""
    fields_to_return = ['id', 'title']
    queryset = InterfaceCase.filter(is_delete=False).all()
    items = await paginate(queryset, fields_to_return, page, page_size)
    return {'code': 200, 'msg': 'ok', 'data': items}


@interface_router.get('/cases/{case_id}/', summary='用例详情')
async def get_interface_case(case_id: int) -> dict:
    """获取接口用例详情"""
    fields_to_return = ['id', 'title', 'interface_id', 'request', 'headers', 'file', 'setup_script', 'teardown_script',
                        'create_time', 'update_time']
    case_obj = await InterfaceCase.get_or_none(id=case_id, is_delete=False).values(*fields_to_return)
    if not case_obj:
        return {'code': 400, 'msg': '用例不存在'}
    fields_to_return_InterfaceManager = ['id', 'name', 'url', 'method', 'type', 'create_time', 'update_time',
                                         'project_id']
    case_obj['interface_id'] = await (InterfaceManager.filter(id=case_obj['interface_id'], is_delete=False).values
                                      (*fields_to_return_InterfaceManager))
    return {'code': 200, 'msg': 'ok', 'data': case_obj}


# @interface_router.post('/cases/run', summary='运行接口用例')
# async def run_interface_case(case: RunCaseSchema) -> dict:
#     """运行接口用例"""
#     env = await TestEnv.get_or_none(id=case.env, is_delete=False)
#     if env:
#         env_data = {
#             "envs": {
#                 **env.global_variables,
#                 **env.debug_global_variable
#             },
#             "headers": env.headers,
#             "db": env.db,
#             "base_url": env.host,
#             "global_func": env.global_func,
#             "functools": open("czdApiTestEngine/test/tools.py", 'r', encoding='utf-8').read(),
#         }
#
#         case_data = [
#             {
#                 'name': "调试运行",
#                 'cases': [case.case.model_dump()]
#             }
#         ]
#         # print(case_data)
#         env.debug_global_variable = env_data.get('envs', {})
#         run_result = testRunner.TestRunner(case_data, env_data).run()
#         # print(run_result)
#         return {'code': 200, 'msg': 'ok', 'data': jsonable_encoder(run_result)}
#     return {'code': 1001, 'msg': 'env is None'}

@interface_router.post('/cases/run', summary='运行接口用例')
async def run_interface_case(case: RunCaseSchema) -> dict:
    """运行接口用例"""
    env = await TestEnv.get_or_none(id=case.env, is_delete=False)
    case_obj = await InterfaceCase.get_or_none(id=case.case, is_delete=False)
    if not env:
        return {'code': 400, 'msg': '环境不存在'}
    if not case_obj:
        return {'code': 400, 'msg': '用例不存在'}
    env_data = {
        "envs": {
            **env.global_variables,
            **env.debug_global_variable
        },
        "headers": env.headers,
        "db": env.db,
        "base_url": env.host,
        "global_func": env.global_func
    }
    case_config = {
        "title": case_obj.title,
        "interface": await InterfaceManager.filter(id=case_obj.interface_id, is_delete=False).first().values('name', 'method', 'url'),
        "headers": case_obj.headers,
        "request": case_obj.request,
        "setup_script": case_obj.setup_script,
        "teardown_script": case_obj.teardown_script
    }
    case_data = [
        {
            'name': "调试运行",
            'cases': [case_config]
        }
    ]
    run_result = testRunner.TestRunner(case_data, env_data).run()
    return {'code': 200, 'msg': 'ok', 'data': jsonable_encoder(run_result)}

