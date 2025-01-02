#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/28 17:31
# @describe:
from .baseCase import BaseCase


class TestResult:

    def __init__(self, all, name='调试运行'):
        self.all = all
        self.name = name
        self.success = 0
        self.fail = 0
        self.error = 0
        self.cases = []

    def addSuccess(self, case: BaseCase):
        """
        执行成功
        :param case: 用例对象
        :return:
        """
        self.success += 1
        info = {
            'name': getattr(case, 'title', ''),
            'method': getattr(case, 'method', ''),
            'url': getattr(case, 'url', ''),
            'status_code': getattr(case, 'status_code', ''),
            'status': 'success',
            'request_headers': getattr(case, 'request_headers', ''),
            'request_body': getattr(case, 'request_body', ''),
            'response_headers': getattr(case, 'response_headers', ''),
            'response_body': getattr(case, 'response_body', ''),
            'log_data': getattr(case, 'log_data', '')
        }
        self.cases.append(info)

    def addFail(self, case: BaseCase):
        self.fail += 1
        info = {
            'name': getattr(case, 'title', ''),
            'method': getattr(case, 'method', ''),
            'url': getattr(case, 'url', ''),
            'status_code': getattr(case, 'status_code', ''),
            'status': 'fail',
            'request_headers': getattr(case, 'request_headers', ''),
            'request_body': getattr(case, 'request_body', ''),
            'response_headers': getattr(case, 'response_headers', ''),
            'response_body': getattr(case, 'response_body', ''),
            'log_data': getattr(case, 'log_data', '')
        }
        self.cases.append(info)

    def addError(self, case: BaseCase):
        self.error += 1
        info = {
            'name': getattr(case, 'title', ''),
            'method': getattr(case, 'method', ''),
            'url': getattr(case, 'url', ''),
            'status_code': getattr(case, 'status_code', ''),
            'status': 'error',
            'request_headers': getattr(case, 'request_headers', ''),
            'request_body': getattr(case, 'request_body', ''),
            'response_headers': getattr(case, 'response_headers', ''),
            'response_body': getattr(case, 'response_body', ''),
            'log_data': getattr(case, 'log_data', '')
        }
        self.cases.append(info)

    def get_result_info(self):
        """
        获取测试集中的用例执行结果
        :return:
        """
        if self.success == self.all:
            state = 'success'
        elif self.error > 0:
            state = 'error'
        else:
            state = 'fail'
        return {
            'state': state,
            'name': self.name,
            'all': self.all,
            'success': self.success,
            'fail': self.fail,
            'error': self.error,
            'cases': self.cases
        }

