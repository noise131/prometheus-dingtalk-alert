# encoding: utf-8

import os
from DingtalkRobot import DingtalkRobot
from YamlConfig import YamlConfig
from LogHandle import LogHandle


# 全局配置存储
class GlobalConfig:
    test_var: int = 1

    '''共享常量'''
    # 默认 config.yaml 位置
    OPTS_YAML_CONFIG_FILE: str = 'config.yaml'
    EXEC_VERSION: str = '2.0'
    EXEC_NAME: str = 'prometheus-dingtalk-alert'

    '''默认配置'''
    DEF_TEMPLATE_PATH: str = 'templates/default-markdown.tmpl'
    DEF_WEBHOOK_ADDRESS: str = '0.0.0.0'
    DEF_WEBHOOK_PORT: str = 8000
    DEF_LOG_LEVEL: list = ['ERROR', 'WARNING', 'INFO', 'DEBUG']

    '''配置变量'''
    # 模板相关配置
    template_path: str = None
    template_folder: str = None
    template_file: str = None
    # webhook 监听相关配置
    webhook_address: str = None
    webhook_port: int = None
    # 日志相关配置
    log_level: list = None
    log_file: str = None
    std_destination: str = None

    '''共享变量'''
    # 共享 dingtalk 机器人对象
    robot_dict: dict = {}
    # 共享 yamlconfig 配置文件处理对象
    yaml_config: YamlConfig = None
    # 共享 loghandle 日志处理对象
    log_handle: LogHandle = None
    # 共享配置信息输出日志对象
    '''
    log_config_out: LogHandle = LogHandle(std_destination=LogHandle.STD_CONCURRENTLY,
                                          log_file_path='logtest.log',
                                          std_level=['NOSTD'],
                                          std_format='%info%')
    '''
    log_config_out: LogHandle = LogHandle(std_level=['DEBUG'], std_format='%info%')

    '''记录变量'''
    # 告警记录变量
    alert_record: dict = {'record': [], 'max': 200}
    # 消息发送记录
    send_record: dict = {'record': [], 'max': 200}


def set_template_config(yaml_config: YamlConfig):
    GlobalConfig.template_path = yaml_config.yaml_config_data.get('template')
    # print(GlobalConfig.template_path)
    if not GlobalConfig.template_path:
        template_path = GlobalConfig.DEF_TEMPLATE_PATH
    GlobalConfig.template_folder, GlobalConfig.template_file = os.path.split(GlobalConfig.template_path)
    GlobalConfig.log_config_out.debug('==> template 配置信息 <==')
    GlobalConfig.log_config_out.debug('template 目录 : {}'.format(GlobalConfig.template_folder))
    GlobalConfig.log_config_out.debug('template 文件 : {}'.format(GlobalConfig.template_file))
    return None


def set_robot_config(yaml_config: YamlConfig):
    robot_list = yaml_config.yaml_config_data.get('dingtalkRobotConfig')
    if not robot_list:
        return {'code': 103, 'info': '获取机器人配置信息失败，至少需要配置一个机器人'}
    robot_instance: dict = {}
    # print(robot_list)
    for robot_instance in robot_list:
        robot_name: str = robot_instance.get('robot')
        if not robot_name:
            return {'code': 104, 'info': '缺少机器人名'}
        webhook_url: str = robot_instance.get('webhook')
        if not webhook_url:
            return {'code': 105, 'info': '缺少机器人 webhook 地址信息'}
        security: dict = robot_instance.get('securityType')
        if not security or type(security) is not dict:
            return {'code': 106, 'info': '缺少机器人 security 信息'}
        message_type: str = robot_instance.get('messageType')
        if not message_type:
            message_type = 'text'
        at_mobiles: list = robot_instance.get('atMobiles')
        if not at_mobiles:
            at_mobiles = []
        at_all: bool = robot_instance.get('atAll')
        if not at_all:
            at_all = False
        # print(at_all)
        GlobalConfig.robot_dict[robot_name] = DingtalkRobot(robot_name, webhook_url, security,
                                                            at_mobiles, at_all, message_type)
    GlobalConfig.log_config_out.debug('==> robot 配置信息 <==')
    i: DingtalkRobot
    for i in GlobalConfig.robot_dict.values():
        GlobalConfig.log_config_out.debug(i.get_config_dict())
    return None


def set_webhook_config(yaml_config: YamlConfig):
    webhook_dict: dict = yaml_config.yaml_config_data.get('webhookListen')
    # 处理 webhook_host 配置
    GlobalConfig.webhook_address = webhook_dict.get('host')
    if not GlobalConfig.webhook_address:
        GlobalConfig.webhook_address = GlobalConfig.DEF_WEBHOOK_ADDRESS
    # 处理 webhook_port 配置
    GlobalConfig.webhook_port = webhook_dict.get('port')
    if not GlobalConfig.webhook_port:
        GlobalConfig.webhook_port = GlobalConfig.DEF_WEBHOOK_PORT
    GlobalConfig.log_config_out.debug('==> webhook 配置信息 <==')
    GlobalConfig.log_config_out.debug('webhook-host : {}'.format(GlobalConfig.webhook_address))
    GlobalConfig.log_config_out.debug('webhook-port : {}'.format(GlobalConfig.webhook_port))
    return None


def set_log_config(yaml_config: YamlConfig):
    status: dict = None
    log_config_dict: dict = yaml_config.yaml_config_data.get('logConfig')
    if log_config_dict:
        if log_config_dict.get('enable'):
            if log_config_dict.get('level'):
                GlobalConfig.log_level = log_config_dict.get('level')
                GlobalConfig.log_config_out.debug('==> log 配置信息')
                GlobalConfig.log_config_out.debug('输出等级 : {}'.format(GlobalConfig.log_level))
            else:
                GlobalConfig.log_level = GlobalConfig.DEF_LOG_LEVEL
                status = {"code": 0, "info": '未指定日志输出等级，将使用默认的输出等级'}
            if log_config_dict.get('logFile'):
                GlobalConfig.log_file = log_config_dict.get('logFile')
                GlobalConfig.std_destination = LogHandle.STD_CONCURRENTLY
                GlobalConfig.log_config_out.debug('日志文件 : {}'.format(GlobalConfig.log_file))
            else:
                GlobalConfig.std_destination = LogHandle.STD_CONSOLE
                status = {"code": 0, "info": '未指定日志文件，将使用控制台输出'}
        else:
            GlobalConfig.log_level = ['NOSTD']
    else:
        GlobalConfig.log_level = ['NOSTD']
    return status


if __name__ == '__main__':
    pass
