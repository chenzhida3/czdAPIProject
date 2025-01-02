#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/27 16:13
# @describe:
from datetime import datetime
from ..test.tools import get_timestamp


class CaseLogHandler:
    """
    日志处理类
    """

    def save_log(self, msg, level):
        if not hasattr(self, 'log_data'):
            setattr(self, 'log_data', [])
        now = datetime.now()
        formatted_timestamp = now.strftime('%Y-%m-%d %H:%M:%S.%f')
        getattr(self, 'log_data').append({'level': level, 'time': formatted_timestamp, 'msg': msg})
        print({'level': level, 'time': formatted_timestamp, 'msg': msg})

    def print_log(self, *args):
        msg = ' '.join([str(i) for i in args])
        self.save_log(msg, 'PRINT')

    def debug_log(self, *args):
        msg = ' '.join([str(i) for i in args])
        self.save_log(msg, 'DEBUG')

    def info_log(self, *args):
        msg = ' '.join([str(i) for i in args])
        self.save_log(msg, 'INFO')

    def error_log(self, *args):
        msg = ' '.join([str(i) for i in args])
        self.save_log(msg, 'ERROR')

    def warning_log(self, *args):
        msg = ' '.join([str(i) for i in args])
        self.save_log(msg, 'WARN')

    def critical_log(self, *args):
        msg = ' '.join([str(i) for i in args])
        self.save_log(msg, 'CRITICAL')


if __name__ == '__main__':
    CaseLogHandler().info_log('sdfs', '撒旦发撒法')
