# encoding: utf-8

from .messageTools import *
from .signTools import *


class DingtalkRobot:
    __robot_name: str = None
    __webhook_url: str = None
    __security_type: dict = None
    # __at_mobiles: List[str] = []
    __at_mobiles: List[str] = None
    __at_all: bool = None
    message_type: str = ''

    __message_response = None
    __headers = {'Content-Type': 'application/json'}

    def __init__(self, robot_name: str, webhook_url: str, security_type: dict, at_mobiles: list = [],
                 at_all: bool = False, message_type: str = 'text'):
        self.__robot_name = robot_name
        self.__webhook_url = webhook_url
        self.__security_type = security_type
        # if self.__security_type['type'] == 'secret':
        #     self.__webhook_url = self.webhook_sign()
        self.__at_mobiles = at_mobiles
        self.__at_all = at_all
        self.message_type = message_type

    def send_text(self, content):
        if type(content) is list:
            content = md_text_machining(content, 1)
            if type(content) is dict:
                return content
        if invalid_message(content):
            return {'error_code': 2, 'error_info': '标题或内容不合法'}
        if self.__security_type['type'] == 'secret':
            webhook_url = self.webhook_sign()
        else:
            webhook_url = self.__webhook_url
        self.__message_response = send_message(webhook_url, self.__headers, self.__security_type, content,
                                               'text', self.__at_mobiles, self.__at_all)
        return self.__send_status_check()

    def send_markdown(self, text, title: str = 'DingtalkMessageTitle'):
        if type(text) is list:
            text = md_text_machining(text, 2)
            if type(text) is dict:
                return text
        if invalid_message(title):
            return {'error_code': 2, 'error_info': '标题或内容不合法'}
        if self.__security_type['type'] == 'secret':
            webhook_url = self.webhook_sign()
        else:
            webhook_url = self.__webhook_url
        self.__message_response = send_message(webhook_url, self.__headers, self.__security_type, text,
                                               'markdown', self.__at_mobiles, self.__at_all, message_title=title)
        return self.__send_status_check()

    def __send_status_check(self) -> dict:
        if type(self.__message_response) is str:
            return {'error_code': 1, 'error_info': self.__message_response}
        elif type(self.__message_response) is dict:
            return self.__message_response

        response_dict = json.loads(self.__message_response.text)
        response_dict['send_data'] = self.__message_response.send_data
        if response_dict['errcode'] != 0:
            return {'error_code': 20, 'error_info': response_dict}
        # print('%s.%s' % (self.__class__.__name__, sys._getframe().f_code.co_name))
        return {'error_code': 0, 'error_info': response_dict}

    def webhook_sign(self) -> str:
        sign_dict = sing_calculation(self.__security_type['value'])
        return '{}&timestamp={}&sign={}'.format(self.__webhook_url, sign_dict['timestamp'], sign_dict['sign'])

    @staticmethod
    def webhook_sign_n(secret: str, webhook_url: str) -> str:
        sign_dict = sing_calculation(secret)
        return '{}&timestamp={}&sign={}'.format(webhook_url, sign_dict['timestamp'], sign_dict['sign'])

    def print_test(self):
        print(self.__dict__)

    def get_config_dict(self):
        dict_cache: dict = {'robot': self.__robot_name, 'webhook': self.__webhook_url,
                            'securityType': self.__security_type, 'messageType': self.message_type,
                            'atMobiles': self.__at_mobiles, 'atAll': self.__at_all}
        # return self.__dict__
        return dict_cache
