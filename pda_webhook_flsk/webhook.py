import json

import DingtalkRobot
import globalConfig
import re
from flask import Flask, request, render_template
from datetime import datetime, timedelta
import jinja2
# from main import webhook_app


webhook_app = Flask('webhook_app', template_folder=globalConfig.CONFIG_TEMPLATE_FOLDER)

# print(__name__)

class AppConfig:
    DEBUG: bool = False


@webhook_app.route(rule='/')
def hello():
    return ''

# @webhook_app.route(rule='/webhook/<robot_name>/send')
# def robot_test(robot_name):
#     dict1 = {}
#     dict1['title'] = 'test'
#     # print(globalConfig)
#     # print(globalConfig.CONFIG_TEMPLATE_FOLDER)
#     print(render_template(globalConfig.CONFIG_TEMPLATE_FILE, **dict1))
#     return render_template(globalConfig.CONFIG_TEMPLATE_FILE, **dict1)
#     # return str(robot_name)


@webhook_app.route(rule='/webhook/<robot_name>/send', methods=['post'])
def webhook_post_handle(robot_name):
    prometheus_json_data: dict = request.json
    # print(request.headers)
    # print('收到一个 post 请求\n', prometheus_json_data)
    for i in range(0, len(prometheus_json_data['alerts'])):
        start_utc = prometheus_json_data['alerts'][i]['startsAt']
        start_cst = datetime.strptime(start_utc, "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(hours=8)
        prometheus_json_data['alerts'][i]['startsAt'] = start_cst.strftime('%Y-%m-%dT%H:%M:%SZ')
        end_utc = prometheus_json_data['alerts'][i]['endsAt']
        try:
            end_cst = datetime.strptime(end_utc, "%Y-%m-%dT%H:%M:%SZ") + timedelta(hours=8)
        except ValueError:
            end_cst = datetime.strptime(end_utc, "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(hours=8)
        prometheus_json_data['alerts'][i]['endsAt'] = end_cst.strftime('%Y-%m-%dT%H:%M:%SZ')
        # print(start_cst, type(start_cst))
        # print()
    for alter in prometheus_json_data['alerts']:
        outstr = render_template(globalConfig.CONFIG_TEMPLATE_FILE, **alter)
        outstr = template_message_split(outstr)
        # print('\n'.join(outstr))
        robot: DingtalkRobot.DingtalkRobot = globalConfig.CONFIG_DINGTALK_ROBOT.get(robot_name)
        if not robot:
            print({'error_code:': 12, 'error_info': '没有找到指定的机器人 : {}'.format(robot_name)})
            return 'Not Found {} robot'.format(robot_name)
        if robot.message_type == 'markdown':
            r = robot.send_markdown(outstr, alter['annotations']['title'])
        else:
            r = robot.send_text(outstr)
        print(r)
    return 'recv success'

def template_message_split(message: str):
    str_list = message.split('\n')
    for i in range(0, len(str_list)):
        str_list[i] = re.sub('^\s+$', '', str_list[i])
    str_list2 = []
    for i in str_list:
        if i:
            str_list2.append(i)
    return str_list2


if __name__ == '__main__':
    webhook_app.config.from_object(AppConfig)
    webhook_app.run(host='0.0.0.0', port=8000)
