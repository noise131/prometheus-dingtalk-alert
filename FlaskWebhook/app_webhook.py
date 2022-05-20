# encoding: utf-8

import re
import jinja2
import datetime
from datetime import datetime, timedelta
from flask import Flask, request, render_template
# from flask_basicauth import BasicAuth
from DingtalkRobot import DingtalkRobot
from GlobalConfig import GlobalConfig
from LogHandle import LogHandle


def test():
    # print(main.EXEC_NAME)
    print('app_webhook', GlobalConfig.test_var)
    GlobalConfig.log_handle.error('webhookTestWrite', 0)


# print(GlobalConfig.template_path)

webhook_app = Flask('app_webhook', template_folder=GlobalConfig.template_folder)


# GlobalConfig.log_handle = LogHandle(LogHandle.STD_CONCURRENTLY,
#                                     log_file_path='logtest.log',
#                                     std_level=['NOSTD'],
#                                     std_app=GlobalConfig.EXEC_NAME)

# webhook_app.config['BASIC_AUTH_USERNAME'] = 'admin'
# webhook_app.config['BASIC_AUTH_PASSWORD'] = '1234567'
#
# webhook_app.config['BASIC_AUTH_USERNAME'] = ''
# webhook_app.config['BASIC_AUTH_PASSWORD'] = ''
#
# webhook_app_basic_auth = BasicAuth(webhook_app)

@webhook_app.route(rule='/')
# @webhook_app_basic_auth.required
def root():
    return {"code": 200, "info": "active"}, 200, [('content-type', 'application/json')]


@webhook_app.route(rule='/webhook/<robot_name>/send', methods=['post', 'get'])
def send(robot_name):
    if request.method not in ('POST', 'post'):
        GlobalConfig.log_handle.warning('不正确的请求方法 : {}, 应为 POST 请求'.format(request.method), 350)
        return {"code": 350, "info": '不正确的请求方法 : {}, 应为 POST 请求'.format(request.method)}, '200', [
            ('content-type', 'application/json')]
    prometheus_json_data: dict = request.json
    robot: DingtalkRobot = GlobalConfig.robot_dict.get(robot_name)
    if not robot:
        GlobalConfig.log_handle.error('没有找到该机器人实例 : {}'.format(robot_name), 330)
        return {"code": 330, "info": '没有找到该机器人实例 : {}'.format(robot_name)}, '200', [
            ('content-type', 'application/json')]
    # robot.send_markdown('1111')
    if not prometheus_json_data.get('alerts'):
        return {"code": 360, "info": '无效数据请求 : {}'.format(prometheus_json_data)}, '200', [
            ('content-type', 'application/json')]
    # print(robot.get_config_dict())
    # 修改 alert 时区
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
        # GlobalConfig.alert_record['record'].append('1')

    # 解析 alert 数据并调用 dingtalk 机器人发信
    for alter in prometheus_json_data['alerts']:
        alert_record(alter)
        GlobalConfig.log_handle.debug('接收到一条 alert {}'.format(alter), 0)
        outstr = render_template(GlobalConfig.template_file, **alter)
        # print(outstr)
        outstr = template_message_split(outstr)
        # print('\n'.join(outstr))
        if robot.message_type == 'markdown':
            title = None
            annotations = alter.get('annotations')
            if annotations:
                title = annotations.get('title')
            if not title:
                title = 'DingtalkMessageTitle'
            r = robot.send_markdown(outstr, title)
            # alter['annotations']['title']
        else:
            r = robot.send_text(outstr)
        # print(r)
        if r.get('error_code') != 0:
            GlobalConfig.log_handle.error('{}'.format(r.get('error_info')), 1)
        send_record(r)
        GlobalConfig.log_handle.debug('发送了一条消息, {}'.format(r), 0)
    # print(prometheus_json_data)
    return '{} send message'.format(robot_name)
    pass


@webhook_app.route(rule='/api/get/send_record')
def api_get_send_record():
    return render_template('send_record.html', **GlobalConfig.send_record)


@webhook_app.route(rule='/api/get/alert_record')
def api_get_alert_record():
    return render_template('alert_record.html', **GlobalConfig.alert_record)


def template_message_split(message: str):
    str_list = message.split('\n')
    for i in range(0, len(str_list)):
        str_list[i] = re.sub('^\s+$', '', str_list[i])
    str_list2 = []
    for i in str_list:
        if i:
            str_list2.append(i)
    return str_list2


def alert_record(record):
    record['time'] = '{}'.format(datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
    if len(GlobalConfig.alert_record['record']) >= GlobalConfig.alert_record['max']:
        del GlobalConfig.alert_record[len(GlobalConfig.alert_record['record']) - 1]
    GlobalConfig.alert_record['record'].insert(0, record)
    # print(GlobalConfig.alert_record)
    pass


def send_record(record):
    del record['error_info']['send_data']
    record['time'] = '{}'.format(datetime.now().strftime('%Y-%m-%dT%H:%M:%S'))
    if len(GlobalConfig.send_record['record']) >= GlobalConfig.send_record['max']:
        del GlobalConfig.send_record[len(GlobalConfig.send_record['record']) - 1]
    GlobalConfig.send_record['record'].insert(0, record)
    # print(GlobalConfig.send_record)
    pass


if __name__ == '__main__':
    webhook_app.run(host='0.0.0.0', port=8000)
    pass
