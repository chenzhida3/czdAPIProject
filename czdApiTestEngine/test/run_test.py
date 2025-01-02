#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/27 11:14
# @describe:

from ..core.baseCase import BaseCase, ENV, tool, db

if __name__ == '__main__':
    case = {
        "title": "用例名称",
        "interface": {
            "url": "/api/book/list",
            "method": "post"
        },
        "headers": {
            "Content-Type": "application/json",
            "X-A-Token": "${{X-A-Token}}"
        },
        "request": {
            "params": {
                "page": '${{page}}',
                "size": '${{size}}',
                "sort": 'create_time',
                "order": "asc"
            },
            "data": {},
            "json": {
                "zh_name": "",
                "sex": 1
            },
            "files": {}
        },
        "setup_script": open("setup_script.txt", 'r', encoding='utf-8').read(),

        "teardown_script": open("teardown_script.txt", 'r', encoding='utf-8').read()

    }
    test_env_db = {
        "base_url": "https://bookmanage-test.webcomicsapp.com",
        "headers": {
            "Content-Type": "application/json",
        },
        "envs": {
            "page": 1,
            "size": 10,
            "X-A-Token": "fIGCU9MVJRoUBnG1sRWEYUfM6+mIYxSD+3W-XmV-M1q7ycKe2vS-EIv7-2TECfmAlgk1v-TtqyOGWIco4ocpA6P31VD0UONIQ3iwamSiVrZeLhxH+DDaIdKbmTXTuJzIQKY2DjDj-0tUrKHniB5FMA=="
        },
        "functools": open("tools.py", 'r', encoding='utf-8').read(),
        "db": [
            {
                "name": "learn",
                "type": "mysql",
                "config": {
                    "host": "127.0.0.1",
                    "port": 3306,
                    "user": "root",
                    "password": "123456"
                }
            },
            {
                "name": "webcomics",
                "type": "mysql",
                "config": {
                    "host": "127.0.0.1",
                    "port": 3306,
                    "user": "root",
                    "password": "123456"
                }
            },
            {
                "name": "mango",
                "type": "mongodb",
                "config": {
                    "host": "18.162.188.202",
                    "port": 10207
                }
            },
            {
                "name": "red",
                "type": "redis",
                "config": {
                    "host": "18.162.188.202",
                    "port": 6379
                }
            }
        ]
    }
    ENV.update(test_env_db)
    exec(ENV["functools"], tool.__dict__)
    db.init_connection(ENV['db'])
    BaseCase().perform(case)
    db.close_db_connection()
