# encoding: utf-8

import json
import random
import requests
from typing import Dict, List


def invalid_message(message: object) -> bool:
    if type(message) is str and message:
        return False
    return True


def at_mobiles_handle(at_mobiles: list) -> str:
    if len(at_mobiles) > 1:
        str_splicing = ''
        for i in range(0, len(at_mobiles)):
            if i == 0:
                str_splicing = '@{}'.format(at_mobiles[i])
                continue
            str_splicing = '{}\n\n@{}'.format(str_splicing, at_mobiles[i])
        return str_splicing
    elif len(at_mobiles) == 1:
        return '@{}'.format(at_mobiles[0])


def send_message(webhook_url: str, headers: dict, security_type: dict, message_text: str, message_type: str, at_mobiles_list: list, at_all: bool, message_title: str = 'title'):
    if security_type['type'] == 'keyword':
        index = random.randrange(0, (len(security_type['value'])))
        # print('----------\n', len(security_type['value']), index, '----------')
        if message_type == 'markdown':
            sep = '\n\n'
        else:
            sep = '\n'
        message_text = '{}{}{}'.format(message_text, sep, security_type['value'][index])

    if at_all:
        at_mobiles_list = []
    else:
        mobiles_check_result: dict = at_mobiles_check(at_mobiles_list)
        if mobiles_check_result['error_code'] != 0:
            return mobiles_check_result

    if message_type == 'markdown':
        if at_mobiles_list:
            at_mobiles_str = at_mobiles_handle(at_mobiles_list)
        else:
            at_mobiles_str = ''
        send_data = {
            "msgtype": 'markdown',
            'markdown': {
                "title": message_title,
                "text": '%s\n\n%s' % (message_text, at_mobiles_str)
            },
            "at": {
                "atMobiles": at_mobiles_list,
                "isAtAll": '%s' % at_all
            }
        }
    else:
        send_data = {
            "msgtype": 'text',
            'text': {
                "content": message_text
            },
            "at": {
                "atMobiles": at_mobiles_list,
                "isAtAll": '%s' % at_all
            }
        }
    try:
        response = requests.post(webhook_url, headers=headers, data=json.dumps(send_data))
    except Exception as e:
        return str(e)
    else:
        response.send_data = send_data
        return response


def at_mobiles_check(at_mobiles: List[str]):
    for i in at_mobiles:
        if type(i) is int:
            return {'error_code': 3, 'error_info': '手机号应为字符类型数据 : %s' % i}
        if not i.isdigit():
            return {'error_code': 3, 'error_info': '手机号内容不合法 : %s' % i}
        if len(i) != 11:
            return {'error_code': 3, 'error_info': '手机号位数缺失 : %s' % i}
    return {'error_code': 0, 'error_info': 'ok'}


def md_text_machining(text_list: list, sep_count: int = 1) -> Dict[str, str] or str:
    sep_str = ''
    for _ in range(1, sep_count + 1):
        sep_str = '{}{}'.format(sep_str, '\n')
    if len(text_list) == 0:
        return {'error_code': 5, 'error_info': '消息 text 内容列表元素不足'}
    elif len(text_list) == 1:
        text_str = ''.join(text_list)
    else:
        text_str = sep_str.join(text_list)
    return text_str

if __name__ == '__main__':
    text_list = ['line1', 'line2', 'line3', 'line4']
    text_list = []
    text_result = md_text_machining(text_list)
    print(text_result)
    print('----------')

