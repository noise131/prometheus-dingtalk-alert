import sys
import re
import optsHandle
import YamlConfig
import DingtalkRobot

from multiprocessing import Process

# 模板文件位置配置
DEF_TEMPLATE: str = 'templates/default_dingtalk-templates.tmpl'
CONFIG_TEMPLATE: str = None
CONFIG_TEMPLATE_FOLDER: str = None
CONFIG_TEMPLATE_FILE: str = None

# 钉钉机器人配置
DEF_DINGTALK_ROBOT: dict = {}
CONFIG_DINGTALK_ROBOT: dict = {}

# webhook 监听配置
DEF_WEBHOOK_HOST: str = '0.0.0.0'
DEF_WEBHOOK_PORT: int = 5000
CONFIG_WEBHOOK_HOST: str = None
CONFIG_WEBHOOK_PORT: int = None

# 日志配置
DEF_LOG_ENABLE: bool = False
DEF_SEND_LOG_FILE: str = 'send.log'
DEF_ERROR_LOG_FILE: str = 'error.log'


def set_config(yaml_obj: YamlConfig.YamlConfig, doc_name: str = 'doc1'):
    set_template_config(yaml_obj, doc_name)
    set_robot_config(yaml_obj, doc_name)
    set_webhook_listen(yaml_obj, doc_name)


def set_webhook_listen(yaml_obj:YamlConfig.YamlConfig, doc_name: str = 'doc1'):
    global CONFIG_WEBHOOK_HOST, CONFIG_WEBHOOK_PORT
    webhook_listen_dict: dict = yaml_obj.get_config_doc(doc_name).get('webhookListen')
    CONFIG_WEBHOOK_HOST = webhook_listen_dict.get('host')
    if not CONFIG_WEBHOOK_HOST:
        CONFIG_WEBHOOK_HOST = DEF_WEBHOOK_HOST
    CONFIG_WEBHOOK_PORT = webhook_listen_dict.get('port')
    if not CONFIG_WEBHOOK_PORT:
        CONFIG_WEBHOOK_PORT = DEF_WEBHOOK_PORT



def set_template_config(yaml_obj: YamlConfig.YamlConfig, doc_name: str = 'doc1'):
    global CONFIG_TEMPLATE, CONFIG_TEMPLATE_FOLDER, CONFIG_TEMPLATE_FILE
    CONFIG_TEMPLATE = yaml_obj.get_config_doc(doc_name).get('template')
    # print(CONFIG_TEMPLATE)
    if CONFIG_TEMPLATE is None:
        print('yaml 文件中没有指定模板文件，将使用默认模板文件 : {}'.format(DEF_TEMPLATE))
        CONFIG_TEMPLATE = DEF_TEMPLATE
    CONFIG_TEMPLATE_FOLDER, CONFIG_TEMPLATE_FILE = template_separate(CONFIG_TEMPLATE)
    # print('---', CONFIG_TEMPLATE_FOLDER, CONFIG_TEMPLATE_FILE)


def set_robot_config(yaml_obj: YamlConfig.YamlConfig, doc_name: str = 'doc1'):
    # print('set_robot_config')
    robot_list = yaml_obj.get_config_doc(doc_name).get('dingtalkRobotConfig')
    for robot_dict_cache in robot_list:
        # print(robot_dict_cache, type(robot_dict_cache))
        robot_name: str = robot_dict_cache.get('robot')
        if not robot_name:
            print('没有指定机器人名')
            sys.exit(2)
        webhook: str = robot_dict_cache.get('webhook')
        if not webhook:
            print('没有指定机器人 webhook 地址')
            sys.exit(2)
        security_type: dict = robot_dict_cache.get('securityType')
        if not security_type:
            print('没有指定加密类型')
            sys.exit(2)
        message_type: str = robot_dict_cache.get('messageType')
        if not message_type:
            message_type = 'text'
        at_mobiles: list = robot_dict_cache.get('atMobiles')
        if not at_mobiles:
            at_mobiles = []
        at_all: bool = robot_dict_cache.get('atAll')
        if not at_all:
            at_all = False
        CONFIG_DINGTALK_ROBOT['{}'.format(robot_name)] = DingtalkRobot.DingtalkRobot \
            (robot_name, webhook, security_type, at_mobiles, at_all, message_type)


def template_separate(template_path: str):
    path_list = template_path.split('/')
    # print(path_list)
    if path_list[0] == '':
        path_list[0] = '/'
    template_file: str = path_list.pop(-1)
    template_folder = ''
    if path_list:
        template_folder = ''
        for index in range(0, len(path_list)):
            if index == 0 and path_list[0] == '/':
                template_folder = '/'
                continue
            if index == 0 and path_list[0] == '.':
                template_folder = './'
                continue
            if index == (len(path_list) - 1):
                template_folder = '{}{}'.format(template_folder, path_list[index])
                continue
            template_folder = '{}{}/'.format(template_folder, path_list[index])
    # print('folder = %s, file = %s' % (template_folder, template_file))
    if not template_folder:
        template_folder = './'
    return template_folder, template_file


yaml_config = YamlConfig.YamlConfig(optsHandle.OPTS_YAML_CONFIG_FILE)
set_config(yaml_config)
