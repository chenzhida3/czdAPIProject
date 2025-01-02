#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/29 15:30
# @describe:

from pydantic import BaseModel, Field, EmailStr

class LoginUserSchema(BaseModel):
    """登录模型"""
    username: str = Field(..., description="用户名", max_length=50, min_length=3)
    password: str = Field(..., description="密码", max_length=50, min_length=6)

class RegisterUserSchema(LoginUserSchema):
    """注册模型"""
    confirm_password: str = Field(..., description="确认密码", max_length=50, min_length=6)
    email: EmailStr = Field(..., description="邮箱")
    is_superuser: bool = False

class UserInfoSchema(BaseModel):
    """用户信息模型"""
    id: int
    username: str
    email: EmailStr
    is_delete: bool
    is_superuser: bool


