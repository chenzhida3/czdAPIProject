#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/30 15:29
# @describe:
from fastapi.encoders import jsonable_encoder

from apps.interface.models import InterfaceManager, InterfaceCase
from apps.project.models import TestEnv
from apps.scenes.models import SceneToCase, TestScene
from czdApiTestEngine import testRunner


async def run_test_scene(env_id, scene_id):
    env_obj = await TestEnv.get_or_none(id=env_id, is_delete=False)
    scene_obj = await TestScene.filter(id=scene_id, is_delete=False).first()
    if env_obj is None:
        return {'code': 400, 'msg': '环境不存在'}
    if scene_obj is None:
        return {'code': 400, 'msg': '业务流不存在'}

    # 组装env_data
    env_data = {
        "envs": {
            **env_obj.global_variables,
            **env_obj.debug_global_variable
        },
        "db": env_obj.db,
        "headers": env_obj.headers,
        "base_url": env_obj.host
    }
    case_list = await SceneToCase.filter(scene_id=scene_id, is_delete=False).all().order_by('sort')
    case_data_list = []
    for step in case_list:
        icase = await InterfaceCase.filter(id=step.icase_id, is_delete=False).first()
        if icase is None:
            return {'code': 400, 'msg': '接口用例不存在'}
        # 组装case_data
        case_data = {
            "title": icase.title,
            "interface": await InterfaceManager.filter(id=icase.interface_id, is_delete=False).first().values('name',
                                                                                                              'method',
                                                                                                              'url'),
            "headers": icase.headers,
            "request": icase.request,
            "setup_script": icase.setup_script,
            "teardown_script": icase.teardown_script
        }
        case_data_list.append(case_data)
    scene_case_data = [
        {
            "name": scene_obj.name,
            "cases": case_data_list
        }
    ]
    run_result = testRunner.TestRunner(scene_case_data, env_data).run()
    return {'code': 200, 'data': jsonable_encoder(run_result), 'msg': 'ok'}