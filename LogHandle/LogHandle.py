# encoding: utf-8

import io
import re
from .tools import *


class LogHandle:
    # 日志输出位置常量定义
    STD_CONSOLE: str = 'console'
    STD_FILE: str = 'file'
    STD_CONCURRENTLY: str = 'concurrently'
    # 默认值定义
    DEF_STD_FORMAT: str = '{{"time": %time%, "app": %app%, "level": %level%, "code": %code%, "info": %info%}}'
    DEF_LEVEL: list = ['ERROR', 'WARNING', 'INFO', 'DEBUG']
    # 类成员变量
    __log_file_path: str = None
    __log_file_fp: io = None
    __std_destination: str = None
    __std_level: list = None
    __std_format: str = None
    __std_app: str = None

    def __init__(
            self,
            std_destination: str = STD_CONSOLE,
            std_level: list = None,
            log_file_path: str = None,
            std_format: str = None,
            std_app: str = None
    ):
        if std_destination:
            self.__std_destination = std_destination
        if log_file_path:
            self.__log_file_path = log_file_path
            # 如果创建日志处理对象时指定了日志文件则打开日志文件
            self.open_file()
        # 如果日志文件打开失败或没有指定日志文件将输出位置修改为控制台
        if self.__log_file_fp is None:
            self.__std_destination = self.STD_CONSOLE
            # print(self.__std_destination)
        if std_level is not None:
            # print(std_level)
            if type(std_level) is not list:
                print({"time": '"{}"'.format(now_time_format()), "app": self.__std_app, "level": "ERROR", "code": 1000, "info":
                    "日志输出等级应为一个列表. 例如 : [\'ERROR\', \'WARNING\', \'INFO\', \'DEBUG\'], 已使用默认输出等级."})
            else:
                self.__std_level = []
                for i in std_level:
                    self.__std_level.append(i.upper())
        else:
            self.__std_level = self.DEF_LEVEL
            # print('默认赋值')
            # print(self.__std_level)
        if std_format:
            self.__std_format = std_format
        else:
            self.__std_format = self.DEF_STD_FORMAT
        if std_app:
            self.__std_app = std_app

    def open_file(self):
        try:
            self.__log_file_fp = open(self.__log_file_path, 'a')
        except Exception as e:
            print({'time': '{}'.format(now_time_format()), 'app': self.__std_app, 'level': 'ERROR', 'code': 1001,
                   'info': '{} 日志文件打开失败 : {}, 已将输出位置定向为控制台.'.format(self.__log_file_path, str(e))})
            # self.__std_destination = self.STD_CONSOLE

    def debug(self, content: str, code: int = 0):
        if 'debug' in self.__std_level or 'DEBUG' in self.__std_level:
            self.__std_log('DEBUG', code, content)

    def info(self, content: str, code: int = 0):
        if 'info' in self.__std_level or 'INFO' in self.__std_level:
            self.__std_log('INFO', code, content)

    def warning(self, content: str, code: int = 0):
        if 'warning' in self.__std_level or 'WARNING' in self.__std_level:
            self.__std_log('WARNING', code, content)

    def error(self, content: str, code: int = 1):
        if 'error' in self.__std_level or 'ERROR' in self.__std_level:
            # print(self.__std_level)
            self.__std_log('ERROR', code, content)

    def __std_log(self, level: str, code: int, content: str):
        if 'nostd' in self.__std_level or 'NOSTD' in self.__std_level:
            return None
        log_format = self.__std_format
        format_list = []
        while True:
            match1 = re.search('%[a-z]*%', log_format)
            if match1 is not None:
                if 'code' not in match1.group(0):
                    log_format = re.sub(match1.group(0), '"{}"', log_format, count=1)
                else:
                    log_format = re.sub(match1.group(0), '{}', log_format, count=1)
                format_list.append(re.sub('%', '', match1.group(0)))
            else:
                break
        # print(log_format)
        data_list = []
        for i in format_list:
            if i == 'time':
                data_list.append(now_time_format())
            elif i == 'app':
                data_list.append(self.__std_app)
            elif i == 'level':
                data_list.append(level)
            elif i == 'code':
                data_list.append(code)
            elif i == 'info':
                data_list.append(content)
            else:
                data_list.append('')
        log_std = log_format.format(*data_list)
        # print('{} {} {} {}'.format(*data_list))
        # print(log_format, type(log_format))
        # print('{{\'time\': {}, \'level\': {}, \'code\': {}, \'info\': {}}}'.format(*data_list))
        if self.__std_destination == self.STD_CONSOLE:
            self.__std_console(log_std)
        elif self.__std_destination == self.STD_FILE:
            self.__std_file(log_std)
        elif self.__std_destination == self.STD_CONCURRENTLY:
            self.__std_console(log_std)
            self.__std_file(log_std)

    def __std_console(self, log_message):
        print(log_message)

    def __std_file(self, log_message):
        self.__log_file_fp.write('{}{}'.format(log_message, '\n'))
        self.__log_file_fp.flush()
