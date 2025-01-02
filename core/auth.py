#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/29 17:33
# @describe:
from datetime import timedelta, datetime
from typing import Union, Optional

from jose import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Header

import settings
from apps.users.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    """密码加密hash"""
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """密码验证"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Union[int, None] = None):
    """生成token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(seconds=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # 设置过期时间
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encode_jwt

async def check_jwt_token(token: Optional[str] = Header(None)):
    """验证token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_402_PAYMENT_REQUIRED,
        detail={
            'code': 1001,
            'message': "无效token或者token已经过期",
            'data': {},
        },
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not token:
        raise credentials_exception
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception
    user = await User().get_or_none(username=username, is_delete=False)
    if user is None:
        raise credentials_exception
    return payload
