#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/30 11:11
# @describe: fastAPI直接用BackgroundTasks，不用celery

from apps.project.models import TestEnv
from czdApiTestEngine.testRunner import TestRunner
from fastapi.encoders import jsonable_encoder
from apps.interface.models import InterfaceCase, InterfaceManager
from apps.scenes.models import SceneToCase
from apps.task.models import TestRecord, TestReport, TestTask


async def run_test_task(env_id, task_id, tester):
    env_obj = await TestEnv.get_or_none(id=env_id, is_delete=False)
    task_obj = await TestTask.get_or_none(id=task_id, is_delete=False)
    if env_obj is None:
        return {'code': 400, 'msg': '环境不存在'}
    if task_obj is None:
        return {'code': 400, 'msg': '任务不存在'}
    env_data = {
        "envs": {
            **env_obj.global_variables,
            **env_obj.debug_global_variable
        },
        "headers": env_obj.headers,
        "db": env_obj.db,
        "base_url": env_obj.host,
        "global_func": env_obj.global_func
    }
    # 创建执行记录
    record = await TestRecord.create(task=task_obj, env=env_obj, tester=tester, statues='执行中')
    # 多对多获取业务流
    scenes_list = await task_obj.scenes.all().values('id', 'name')

    task_case_data = []
    for scene in scenes_list:
        case_data_list = []
        task_case_data.append({
            "name": scene['name'],
            "cases": case_data_list
        })
        scenes_case_list = await SceneToCase.filter(scene_id=scene['id'], is_delete=False).all().order_by('sort')
        for step in scenes_case_list:
            icase = await InterfaceCase.filter(id=step.icase_id, is_delete=False).first()
            if icase is None:
                return {'code': 400, 'msg': '接口用例不存在'}
            # 组装case_data
            case_data = {
                "title": icase.title,
                "interface": await InterfaceManager.filter(id=icase.interface_id, is_delete=False).first().values(
                    'name', 'method', 'url'),
                "headers": icase.headers,
                "request": icase.request,
                "setup_script": icase.setup_script,
                "teardown_script": icase.teardown_script
            }
            case_data_list.append(case_data)
    # 运行
    run_result = TestRunner(task_case_data, env_data).run()

    # 更新执行记录
    result = {
        "all": 0,
        "success": 0,
        "fail": 0,
        "error": 0,
        "pass_rate": 0,
        "statues": '完成'
    }
    for res in run_result:
        result['all'] += res['all']
        result['success'] += res['success']
        result['fail'] += res['fail']
        result['error'] += res['error']
    result["pass_rate"] = '{:.2}'.format(result['success'] / result['all'])
    # 更新执行记录
    record = await record.update_from_dict(result)
    await record.save()
    # 保存测试报告
    info = {'code': 200, 'message': 'ok', 'data': jsonable_encoder(run_result)}
    await TestReport.create(record=record, info=info)
    return info
