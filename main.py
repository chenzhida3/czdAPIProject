#!/usr/bin/env python
import asyncio
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import settings
from tortoise.contrib.fastapi import register_tortoise
from contextlib import asynccontextmanager


from apps.cronjob.api import cronjob_router
from apps.users.api import user_router
from apps.project.api import project_router
from apps.interface.api import interface_router
from apps.scenes.api import scenes_router
from apps.task.api import task_router
from apps.cronjob.api import scheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

# 注册路由
app.include_router(user_router, prefix='/api/user', tags=['用户模块'])
app.include_router(project_router, prefix='/api/testPro', tags=['项目模块'])
app.include_router(interface_router, prefix='/api/interface', tags=['接口模块'])
app.include_router(scenes_router, prefix='/api/testFlow', tags=['业务流模块'])
app.include_router(task_router, prefix='/api/testTask', tags=['测试任务模块'])
app.include_router(cronjob_router, prefix='/api/cornJob', tags=['定时任务模块'])

# 注册tortoiseORM模型
register_tortoise(
    app,
    config=settings.TORTOISE_ORM,
    modules={"models": ["models"]}
)

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def index():
    return {'message': 'Hello World'}


if __name__ == '__main__':

    uvicorn.run(app, host='127.0.0.1', port=8800)