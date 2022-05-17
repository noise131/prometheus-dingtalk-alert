import DingtalkRobot
import globalConfig

from flask import request
from .webhook import webhook_app


@webhook_app.route(rule='/api/get/config/robot', methods=['get'])
def test():
    robot_name_list = request.args.getlist('name')
    if not robot_name_list:
        return str({'error_code': 100, 'error_info': 'api使用方法有误，请至少指定一个机器人 name 参数'})
    get_result = []
    print(robot_name_list)
    for i in robot_name_list:
        print(i)
        robot_config: DingtalkRobot.DingtalkRobot = globalConfig.CONFIG_DINGTALK_ROBOT.get(i)
        if not robot_config:
            get_result.append(str({'error_code': 30, 'error_info': '没有 {} 机器人的配置信息'.format(str(i))}))
            continue
        get_result.append(str(robot_config.get_config_dict()))
    return '<br/>\n'.join(get_result)

# @webhook_app.route(rule='/api/get/config/<robot_name>', methods=['get'])
# def test(robot_name):
#     robot_config: DingtalkRobot.DingtalkRobot = globalConfig.CONFIG_DINGTALK_ROBOT.get(robot_name)
#     if not robot_config:
#         return str({'error_code': 30, 'error_info': '没有 {} 机器人的配置信息'.format(str(robot_name))})
#     return str(robot_config.get_config_dict())
