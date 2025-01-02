#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/2 17:03
# @describe:
from datetime import datetime


# 创建分页函数
async def paginate(queryset, fields_to_return: list[str], page: int = None, page_size: int = None):
    """
    分页函数
    :param fields_to_return: 返回的字段
    :param queryset: 查询集
    :param page: 页码
    :param page_size: 每页数量
    :return:
    """
    if page is None or page_size is None:
        items = await queryset.all().values(*fields_to_return)
        return items
    offset = (page - 1) * page_size
    total = await queryset.count()
    if total <= page * page_size:
        next_page = False
    else:
        next_page = True
    items = await queryset.offset(offset).limit(page_size).all().values(*fields_to_return)

    return {"total": total, "page": page, "next_page": next_page, "items": items}



if __name__ == '__main__':
    print(datetime.now())