# encoding: utf-8

import sys
import getopt
from GlobalConfig import *


def opts_help():
    help_info = '''\nUsage : prometheus-dingtalk-alert [-hv] [-c CONFIG_FILE]\n
    -h, --help                : 显示帮助信息
    -v, --version             : 显示当前程序的版本
    -c, --config CONFIG_FILE  : 指定 yaml 配置文件位置
                                default : config.yaml\n'''
    print(help_info)


if __name__ == '__main__':
    # 读取命令行参数
    try:
        opts, other_args = getopt.getopt(sys.argv[1:], 'hvc:', ['help', 'version', 'config'])
    except getopt.GetoptError as e:
        r = str(e).split()
        print('[ERROR] Unknown option : \'%s\'' % (r[1]))
        sys.exit(1)
    if other_args:
        print('[ERROR] Parameters that should not appear : \'%s\'' % (other_args[0]))
        sys.exit(1)
    for opts_l, args_l in opts:
        if opts_l in ('-h', '--help'):
            opts_help()
            sys.exit(0)
        elif opts_l in ('-v', '--version'):
            print('{} : {}'.format(GlobalConfig.EXEC_NAME, GlobalConfig.EXEC_VERSION))
            sys.exit(0)
        elif opts_l in ('-c', '--config'):
            GlobalConfig.OPTS_YAML_CONFIG_FILE = args_l
    # print(GlobalConfig.OPTS_YAML_CONFIG_FILE)

    # 读取 yaml 文件配置
    GlobalConfig.yaml_config = YamlConfig(GlobalConfig.OPTS_YAML_CONFIG_FILE)
    if GlobalConfig.yaml_config.get_status() is not None:
        print(GlobalConfig.yaml_config.get_status())
        sys.exit(GlobalConfig.yaml_config.get_status().get('code'))
    # 加载全局配置
    GlobalConfig.log_config_out.debug('----------配置信息输出----------')
    r = set_log_config(GlobalConfig.yaml_config)
    # 创建日志操作对象
    GlobalConfig.log_handle = LogHandle(GlobalConfig.std_destination,
                                        std_level=GlobalConfig.log_level,
                                        log_file_path=GlobalConfig.log_file,
                                        std_app=GlobalConfig.EXEC_NAME)
    if r:
        GlobalConfig.log_handle.warning(r['info'], r['code'])
    set_template_config(GlobalConfig.yaml_config)
    r = set_robot_config(GlobalConfig.yaml_config)
    if r:
        GlobalConfig.log_handle.error(r['info'], r['code'])
        sys.exit(3)
    set_webhook_config(GlobalConfig.yaml_config)
    GlobalConfig.log_config_out.debug('----------配置信息输出----------')
    # print(GlobalConfig.template_folder)
    # print(GlobalConfig.template_path)
    # 所有配置初始化成功后导入并启动 flask
    GlobalConfig.log_handle.info('程序初始化完成, 已启动', 0)
    import FlaskWebhook
    # 启动 flask
    try:
        FlaskWebhook.webhook_app.run(host=GlobalConfig.webhook_address, port=int(GlobalConfig.webhook_port))
        # GlobalConfig.log_handle.debug('webhook启动成功. 监听地址 : {}, 监听端口 : {}'.format(GlobalConfig.webhook_address,
        #                                                                          GlobalConfig.webhook_port))
    except Exception as e:
        GlobalConfig.log_handle.error('{}'.format(e), 320)
