#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/27 16:29
# @describe:
import uuid

from fastapi import APIRouter, Depends, HTTPException
from apps.cronjob.models import CronJob
from apps.cronjob.schemas import CronJobAddSchema, CronJobDeleteSchema, CronJobChangeStatusSchema, CronJobUpdateSchema
from apps.project.models import TestProject, TestEnv
from apps.task.models import TestTask
from core.auth import check_jwt_token
from settings import REDIS
from pytz import timezone
from tortoise import transactions

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.triggers.cron import CronTrigger
from ..task.tasks import run_test_task

cronjob_router = APIRouter(
    dependencies=[Depends(check_jwt_token)]
)

local_timezone = timezone('Asia/Shanghai')
# 配置apscheduler
job_stores = {
    'default': RedisJobStore(host=REDIS.get('host'), port=REDIS.get('port'),
                             password=REDIS.get('password'), db=REDIS.get('db'))
}

job_defaults = {
    'coalesce': False,
    'max_instances': 10
}
# 创建一个异步调度器
scheduler = AsyncIOScheduler(jobstores=job_stores, job_defaults=job_defaults, timezone=local_timezone)


async def run_task(env_id, task_id, tester):
    print('开始执行定时任务:', env_id, task_id)
    await run_test_task(env_id=env_id, task_id=task_id, tester=tester)
    print('定时任务已提交')


@cronjob_router.post("/job/create", summary='创建定时任务')
async def create_cronjob(cronjob: CronJobAddSchema):
    """
    创建定时任务
    """
    cronjob_rule = cronjob.rule.split(' ')
    if len(cronjob_rule) != 5:
        return {'code': 400, 'msg': '规则格式不正确'}
    project_obj = await TestProject.get_or_none(id=cronjob.project, is_delete=False)
    if project_obj is None:
        return {'code': 400, 'msg': '项目不存在'}
    env_obj = await TestEnv.get_or_none(id=cronjob.env, is_delete=False)
    if env_obj is None:
        return {'code': 400, 'msg': '环境不存在'}
    task_obj = await TestTask.get_or_none(id=cronjob.task, is_delete=False)
    if task_obj is None:
        return {'code': 400, 'msg': '任务不存在'}
    job_id = str(uuid.uuid4())
    async with transactions.in_transaction() as tra:
        # 开启数据库事务
        try:
            # 由"30 20 * * *"切割成['30', '20', '*', '*', '*']
            trigger = CronTrigger(minute=cronjob_rule[0], hour=cronjob_rule[1], week=cronjob_rule[2],
                                  day=cronjob_rule[3], month=cronjob_rule[4], timezone=local_timezone)
            scheduler.add_job(func=run_task, trigger=trigger, id=job_id,
                              kwargs={"env_id": env_obj.id, "task_id": task_obj.id, "tester": project_obj.leader})

            # 保存数据库
            cron = await CronJob.create(env=env_obj, job_id=job_id, name=cronjob.name, project=project_obj,
                                        rule=cronjob.rule, status=cronjob.status, task=task_obj)

        except Exception as e:
            await tra.rollback()
            raise HTTPException(status_code=400, detail=str(e))
        else:
            await tra.commit()
            return {'code': 200, 'msg': 'ok', 'data': cron}


@cronjob_router.get("/job/all", summary='获取定时任务列表')
async def get_cronjob_list():
    cronjob_list = await CronJob.filter(is_delete=False).all()
    data_list = []
    for cronjob in cronjob_list:
        data_list.append({
            "id": cronjob.id,
            "name": cronjob.name,
            "project": await TestProject.filter(id=cronjob.project_id).first().values('id', 'name'),
            "env": await TestEnv.filter(id=cronjob.env_id).first().values('id', 'name'),
            "task": await TestTask.filter(id=cronjob.task_id).first().values('id', 'name'),
            "rule": cronjob.rule,
            "status": cronjob.status,
            "job_id": cronjob.job_id,
            "create_time": cronjob.create_time
        })
    return {'code': 200, 'msg': 'ok', 'data': data_list}


@cronjob_router.post("/job/delete", summary='删除定时任务')
async def delete_cronjob(cron: CronJobDeleteSchema):
    """
    删除定时任务
    """
    cronjob = await CronJob.get_or_none(job_id=cron.job_id, is_delete=False)
    if cronjob is None:
        return {'code': 400, 'msg': '定时任务不存在'}
    scheduler.remove_job(cron.job_id)
    await CronJob.filter(job_id=cron.job_id, is_delete=False).update(is_delete=True)
    return {'code': 200, 'msg': 'ok'}


@cronjob_router.post("/job/status", summary='启动和暂停定时任务')
async def change_cronjob_status(cron: CronJobChangeStatusSchema):
    """启动和暂停定时任务"""
    cronjob = await CronJob.get_or_none(job_id=cron.job_id, is_delete=False)
    if cronjob is None:
        return {'code': 400, 'msg': '定时任务不存在'}
    async with transactions.in_transaction() as tra:
        try:
            if cron.status:
                scheduler.resume_job(cron.job_id)
                await CronJob.filter(job_id=cron.job_id, is_delete=False).update(status=True)
            else:
                scheduler.pause_job(cron.job_id)
                await CronJob.filter(job_id=cron.job_id, is_delete=False).update(status=False)
        except Exception as e:
            await tra.rollback()
            raise HTTPException(status_code=400, detail=str(e))
        else:
            await tra.commit()
        return {'code': 200, 'msg': 'ok'}


@cronjob_router.post("/job/update", summary='修改定时任务')
async def update_cronjob(cron: CronJobUpdateSchema):
    """修改定时任务"""
    if len(cron.rule.split(' ')) != 5:
        return {'code': 400, 'msg': '规则格式不正确'}
    cronjob = await CronJob.get_or_none(id=cron.id, is_delete=False)
    if cronjob is None:
        return {'code': 400, 'msg': '定时任务不存在'}
    project_obj = await TestProject.get_or_none(id=cron.project, is_delete=False)
    if project_obj is None:
        return {'code': 400, 'msg': '项目不存在'}
    env_obj = await TestEnv.get_or_none(id=cron.env, is_delete=False)
    if env_obj is None:
        return {'code': 400, 'msg': '环境不存在'}
    task_obj = await TestTask.get_or_none(id=cron.task, is_delete=False)
    if task_obj is None:
        return {'code': 400, 'msg': '任务不存在'}
    result = {
        "id": cron.id,
        "name": cron.name,
        "project": await TestProject.filter(id=cron.project).first().values('id', 'name'),
        "env": await TestEnv.filter(id=cron.env).first().values('id', 'name'),
        "task": await TestTask.filter(id=cron.task).first().values('id', 'name'),
        "rule": cron.rule,
        "status": cron.status,
        "job_id": cronjob.job_id,
        "create_time": cronjob.create_time
    }
    async with transactions.in_transaction() as tra:
        try:
            if cron.status:
                scheduler.resume_job(cronjob.job_id)
            else:
                scheduler.pause_job(cronjob.job_id)
            if cron.rule != cronjob.rule:
                scheduler.reschedule_job(cronjob.job_id, trigger=CronTrigger(minute=cron.rule.split(' ')[0],
                                                                             hour=cron.rule.split(' ')[1],
                                                                             week=cron.rule.split(' ')[2],
                                                                             day=cron.rule.split(' ')[3],
                                                                             month=cron.rule.split(' ')[4],
                                                                             timezone=local_timezone))

            await CronJob.filter(id=cron.id, is_delete=False).update(
                env=env_obj, name=cron.name, project=project_obj, rule=cron.rule, status=cron.status, task=task_obj)
        except Exception as e:
            await tra.rollback()
            raise HTTPException(status_code=400, detail=str(e))
        else:
            await tra.commit()
        return {'code': 200, 'msg': 'ok', 'data': result}


if __name__ == '__main__':
    rule = "30 20 * * *"
    print(rule.split(' '))
