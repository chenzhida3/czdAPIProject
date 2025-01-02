#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/29 15:30
# @describe:

from fastapi import APIRouter
from .schemas import RegisterUserSchema, UserInfoSchema, LoginUserSchema
from .models import User
from core.auth import get_password_hash, verify_password, create_access_token

user_router = APIRouter()


@user_router.post('/register', summary='用户注册')
async def register(user: RegisterUserSchema):
    if user.password != user.confirm_password:
        return {'code': 400, 'msg': '两次密码不一致'}
    if await User().get_or_none(username=user.username):
        return {'code': 400, 'msg': '用户名已存在'}
    if await User().get_or_none(email=user.email):
        return {'code': 400, 'msg': '邮箱已存在'}
    user.password = get_password_hash(user.password)
    user_obj = await User().create(**user.dict())
    return UserInfoSchema(**user_obj.__dict__)


@user_router.post('/login', summary='用户登录')
async def login(user: LoginUserSchema):
    u = await User().get_or_none(username=user.username, is_delete=False)
    if not u:
        return {'code': 400, 'msg': '用户不存在'}
    if not verify_password(user.password, u.password):
        return {'code': 400, 'msg': '密码错误'}
    user_obj = await User().get_or_none(username=user.username)
    token = create_access_token(data={"username": user_obj.username})
    return {'code': 200, 'msg': '登录成功', 'data': {'username': user_obj.username, 'token': token}}
