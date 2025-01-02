#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/28 17:13
# @describe:
import json

from czdApiTestEngine.core.baseCase import db, ENV, tool, BaseCase
from czdApiTestEngine.core.testResult import TestResult


class TestRunner:

    def __init__(self, cases, env_data):
        """
        :param cases:执行的测试用例集
        :param env_data: 环境数据
        """
        self.cases = cases
        self.env_data = env_data
        self.result = []

    def run(self):
        # 初始化数据库连接
        db.init_connection(self.env_data.pop("db"))
        # 遍历所有测试用例集
        for suite in self.cases:
            ENV.clear()
            ENV.update(self.env_data)
            exec(getattr(ENV, "functools", ''), tool.__dict__)
            print("测试套件：", suite['name'])
            result = TestResult(len(suite['cases']), suite['name'])
            for case in suite['cases']:
                self.perform(case, result)
            self.result.append(result.get_result_info())
        db.close_db_connection()

        return self.result

    @staticmethod
    def perform(case, result):
        c = BaseCase()

        try:
            c.perform(case)
        except AssertionError as e:
            result.addFail(c)
        except Exception as e:
            result.addError(c)
        else:
            result.addSuccess(c)


if __name__ == '__main__':
    cases = [
        {
            "name": '测试集合1',
            "cases": [{
                "title": "用例名称1",
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
                "setup_script": open("test/setup_script.txt", 'r', encoding='utf-8').read(),

                "teardown_script": open("test/teardown_script.txt", 'r', encoding='utf-8').read()

            }, {
                "title": "用例名称2",
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
                "setup_script": "",

                "teardown_script": ""

            }]
        },
        {
            "name": '测试集合2',
            "cases": [{
                "title": "用例名称3",
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
                "setup_script": "",

                "teardown_script": ""

            }, {
                "title": "用例名称4",
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
                "setup_script": "",

                "teardown_script": ""

            }]
        },
    ]
    env_data = {
        "base_url": "https://bookmanage-test.webcomicsapp.com",
        "headers": {
            "Content-Type": "application/json",
        },
        "envs": {
            "page": 1,
            "size": 10,
            "X-A-Token": "fIGCU9MVJRoUBnG1sRWEYUfM6+mIYxSD+3W-XmV-M1q7ycKe2vS-EIv7-2TECfmAlgk1v-TtqyOGWIco4ocpA6P31VD0UONIQ3iwamSiVrZeLhxH+DDaIdKbmTXTuJzIQKY2DjDj-0tUrKHniB5FMA=="
        },
        "functools": open("test/tools.py", 'r', encoding='utf-8').read(),
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
    result = TestRunner(cases, env_data).run()
    print("-" * 200)
    print(result)
