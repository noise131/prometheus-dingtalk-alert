import yaml
import sys
from typing import Dict

from .yamlReadTools import *


class YamlConfig():
    yaml_file_path: str = None
    yaml_file_status: Dict[str, str] = {'error_code': 0, 'error_info': ''}
    __yaml_file_fp = None
    __yaml_all_config_data = None
    yaml_config_data: dict = {}

    def __init__(self, yaml_file_path: str):
        self.yaml_file_path = yaml_file_path
        if self.__open_yaml_file():
            self.yaml_file_status['error_info'] = '{} 文件 {} {};'.format(self.yaml_file_status['error_info'],
                                                                        self.yaml_file_path, '打开成功')
            self.__read_yaml_file()

    def __read_yaml_file(self) -> None:
        try:
            self.__yaml_all_config_data = yaml.load_all(self.__yaml_file_fp, Loader=yaml.FullLoader)
        except (yaml.parser.ParserError, yaml.scanner.ScannerError) as e:
            print('[ERROR] - yaml 配置出错 :', yaml_error_info(str(e)))
            sys.exit(2)

        # if type(self.__yaml_all_config_data) is not list:
        #     print(type(self.__yaml_all_config_data))
        #     print('[ERROR] - %s is not a effective yaml format config file' % self.yaml_file_path)
        #     sys.exit(2)
        i = 1
        try:
            for doc_config_data in self.__yaml_all_config_data:
                if doc_config_data.get('doc'):
                    self.yaml_config_data['{}'.format(doc_config_data['doc'])] = doc_config_data
                else:
                    self.yaml_config_data['doc{}'.format(i)] = doc_config_data
                # print(self.yaml_config_data['doc{}'.format(i)])
                i += 1
            # print(all_data)
            self.__yaml_file_fp.close()
            return None
        except Exception as e:
            print('[ERROR] - %s is not a effective yaml format config file; %s' % (self.yaml_file_path, e))
            self.__yaml_file_fp.close()
            sys.exit(2)

    def __open_yaml_file(self) -> bool:
        try:
            self.__yaml_file_fp = open(self.yaml_file_path)
        except Exception as e:
            self.yaml_file_status['error_info'] = str(e)
            return False
        return True

    def print_file_status(self) -> None:
        print(self.yaml_file_status)
        return None
        # print()
        # print(self.__yaml_file_fp)

    def get_config_doc(self, doc_name: str) -> (dict, None):
        return get_yaml_doc(self.yaml_config_data, doc_name)


