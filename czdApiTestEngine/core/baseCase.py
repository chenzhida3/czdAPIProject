#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/26 10:40
# @describe:
import re
import requests
from jsonpath import jsonpath
from . import testTools as tool
from .caseLog import CaseLogHandler
from .DBClient import DBClient

ENV = {}
db = DBClient()

class BaseCase(CaseLogHandler):

    def __run_script(self, data):
        """
        创建生成器，使之后置脚本的可以访问前置脚本的变量
        :param data:
        :return:
        """
        test = self
        envs = ENV.get('envs')
        print = self.print_log
        setup_script = data.get('setup_script')
        # 使用执行器函数执行python的脚本
        exec(setup_script)
        response = yield
        teardown_script = data.get('teardown_script')
        exec(teardown_script)
        yield

    def __setup_script(self, data):
        """
        脚本执行前
        :param data:
        :return:
        """
        self.script_hook = self.__run_script(data)
        next(self.script_hook)

    def __teardown_script(self, response):
        """
        脚本执行后
        :param response:
        :return:
        """
        # next(self.script_hook)
        self.script_hook.send(response)
        # 删除生成器对象
        delattr(self, 'script_hook')

    def __heandle_request_data(self, data):
        """
        处理请求参数
        requests.request(url, data=None, json=None, headers=None **kwargs)
        :param data:
        :return:
        """
        request_data = {'method': data['interface']['method'].lower()}

        # 1、处理请求的url
        url = data['interface']['url']
        if not url.startswith('http'):
            url = ENV.get('base_url') + url
        request_data['url'] = url

        # 2、处理请求头
        headers: dict = ENV.get('headers')
        headers.update(data['headers'])
        request_data['headers'] = headers

        # 3、处理请求参数
        request = data['request']
        # 查询参数
        request_data['params'] = request.get('params')
        # 请求体参数（json/表单/文件上传）
        if headers.get('Content-Type') == 'application/json':
            request_data['json'] = request.get('json', {})
        elif headers.get('Content-Type') == 'application/x-www-form-urlencoded':
            request_data['data'] = request.get('data')
        elif 'multipart/form-data' in headers.get('Content-Type'):
            request_data['files'] = request.get('files')

        return request_data

    def replace_data(self, data):
        """
        替换用例中的变量
        {'method': 'post', 'url': 'https://test.mangaina.com/api/new/user/login', 'headers': {'Content-Type': 'application/json', 'info': '${{token}}'}, 'params': {}, 'json': {'type': 7, 'email': '${{email}}', 'password': '${{password}}'}}
        :param data:
        :return:
        """
        pattern = r'\${{(.+?)}}'
        data = str(data)
        while re.search(pattern, data):
            # 获取匹配到的内容
            match = re.search(pattern, data)
            key = match.group(1)
            try:
                value = ENV.get('envs').get(key)
            except Exception as e:
                return self.error_log('没有找到变量：', key)
            data = data.replace(match.group(), str(value))
        return eval(data)

    def __send_request(self, data):
        """
        发生请求的方法
        :param data:
        :return:
        """
        request_data = self.__heandle_request_data(data)
        # self.log_data(request_data)
        replace_data = self.replace_data(request_data)
        self.info_log(replace_data)
        response = requests.request(**replace_data)
        self.title = data.get('title')
        self.info_log(response.json())
        self.url = response.request.url
        self.method = response.request.method
        self.request_headers = response.request.headers
        self.response_headers = response.request.headers
        self.request_body = response.request.body
        self.response_body = response.json()
        self.status_code = response.status_code
        self.info_log('请求地址：', self.url)
        self.info_log('请求方法：', self.method)
        self.info_log('请求头', self.request_headers)
        self.info_log('请求体：', self.request_body)
        self.info_log('响应头：', self.response_headers)
        self.info_log('响应体：', self.response_body)
        self.info_log('响应状态码：', self.status_code)
        return response

    def perform(self, data):
        """
        执行用例
        :param data:
        :return:
        """
        self.__setup_script(data)
        res = self.__send_request(data)
        self.__teardown_script(res)

    def save_global_variable(self, key, value):
        """保存全局变量"""
        ENV['envs'][key] = value
        self.info_log('保存全局变量:', key, value)

    def delete_global_variable(self, key):
        """删除全局变量"""
        del ENV['envs'][key]
        self.info_log('删除全局变量：', key)

    def json_extract(self, obj, ext):
        """
        提取json数据的方法，返回提取到的值
        :param obj:
        :param ext:
        :return:
        """
        self.info_log('------通过jsonpath提取数据：', ext)
        res = jsonpath(obj, ext)
        value = res[0] if res else ''
        self.info_log('提取到的数据：', value)
        return value

    def json_extract_list(self, obj, ext):
        """
        提取json数据的方法，返回所有提取到的值列表
        :param obj:
        :param ext:
        :return
        """
        self.info_log('------通过jsonpath提取数据：', ext)
        res = jsonpath(obj, ext)
        value = res if res else []
        self.info_log('提取到的数据：', value)
        return value

    def list_extract(self, list_data, key):
        """列表内提取值"""
        self.info_log('------通过list提取数据：', list_data)
        value = [item.get(key) for item in list_data]
        self.info_log('提取到的数据：', value)
        return value

    def re_extract(self, obj, ext):
        """
        提取正则表达式数据的方法，返回提取到的数据值
        :param obj: 数据源
        :param ext:正则提取表达式
        :return:
        """
        self.info_log("----通过正则表达式提取数据:", ext)
        if not isinstance(obj, str):
            obj = str(obj)
        self.info_log("数据源：", obj)
        value = re.search(ext, obj)
        value = value.group(1) if value else ''
        self.info_log('提取的数据值为：', value)
        return value

    def assertion(self, method, expected, actual):
        """
        :param method: 断言的方法
        :param expected: 逾期结果
        :param actual: 实际结果的值
        :return:
        """
        method_map = {
            '相等': lambda x, y: x == y,
            '不相等': lambda x, y: x != y,
            '大于': lambda x, y: x > y,
            '大于等于': lambda x, y: x >= y,
            '小于': lambda x, y: x < y,
            '小于等于': lambda x, y: x <= y,
            '不包含': lambda x, y: x not in y,
            '包含': lambda x, y: x in y,
        }
        assert_func = method_map.get(method)
        if assert_func is None:
            self.info_log("不支持的断言方法：", method)
            return
        else:
            self.info_log("断言比较方法为：", method)
            self.info_log("预期结果:", expected)
            self.info_log("实际结果:", actual)
        try:
            assert assert_func(expected, actual)
        except AssertionError:
            raise AssertionError("断言失败，预期结果为：{},实际结果为：{}".format(expected, actual))
        else:
            self.info_log("断言成功，预期结果为：", expected, "实际结果为：", actual)
