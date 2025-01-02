#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/27 9:51
# @describe: 工具函数
import time
from faker import Faker

fake = Faker(locale='zh_CN')

def random_mobile():
    """随机生成手机号"""
    return fake.phone_number()

def random_email():
    """随机生成邮件"""
    return fake.email()

def random_name():
    """随机生成姓名"""
    return fake.name()

def get_timestamp():
    """获取时间戳"""
    return int(time.time())

def add_number(a, b):
    return a + b


if __name__ == '__main__':
    a = get_timestamp()
    print(a)