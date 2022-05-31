# encoding: utf-8

import io
import yaml
import re


def yaml_error_info(str1):
    str2 = ''
    for i in str1.split('\n'):
        str3, count = re.subn(r'^\s+', '', i)
        if count:
            str2 = '{}{}{}'.format(str2, str3, '; ')
        else:
            str2 = '{}{}{}'.format(str2, str3, ' ')
    return str2


class YamlConfig:
    file_path: str = None
    __file_name: str = None
    __file_fp: io = None
    __doc_name: str = None
    yaml_config_data: dict = None
    __fail: dict = None

    def __init__(self, file_path: str, doc_name: str = 'doc-1'):
        self.file_path = file_path
        self.__doc_name = doc_name
        self.__open_file()
        if not self.__fail:
            self.__read_yaml_file()
        else:
            # print(self.__fail)
            pass

    def __open_file(self):
        # 打开 yaml 配置文件
        try:
            self.__file_fp = open(self.file_path)
        except Exception as e:
            self.__fail = {'status': False, 'code': 100, 'info': '文件 {} 打开失败, {}'.format(self.file_path, str(e))}

    def __read_yaml_file(self):
        # 读取 yaml 配置文件中所有文档
        try:
            yaml_all_config_data = yaml.load_all(self.__file_fp, Loader=yaml.FullLoader)
            # print(yaml_all_config_data)
        except (yaml.parser.ParserError, yaml.scanner.ScannerError) as e:
            # 出现异常报错语法错误
            self.__fail = {'status': False, 'code': 101, 'info': 'yaml 语法错误'.format(yaml_error_info(str(e)))}
            # print(self.__fail)
            # sys.exit(2)
            return
        i = 1
        self.yaml_config_data = {}
        yaml_config_all_dict = {}
        # 将文档逐个解析并添加到字典中，键名为文档中 doc 的建值，如果文档中没有 doc 键则使用 doc-1、doc-2 以此类推作为文档的键名
        try:
            for doc_config_data in yaml_all_config_data:
                # print('x', doc_config_data)
                if doc_config_data.get('doc'):
                    # self.yaml_config_data['{}'.format(doc_config_data['doc'])] = doc_config_data
                    yaml_config_all_dict['{}'.format(doc_config_data['doc'])] = doc_config_data
                else:
                    yaml_config_all_dict['doc-{}'.format(i)] = doc_config_data
                # print(self.yaml_config_data['doc{}'.format(i)])
                i += 1
            # 获取指定文档到 yaml_config_data 变量
            self.yaml_config_data = yaml_config_all_dict.get(self.__doc_name)
            # for i in self.yaml_config_data.items():
            #     print(i, end='\n\n')
            self.__file_fp.close()
            # 出现异常报错无效 yaml 格式
        except Exception as e:
            self.__fail = {'status': False, 'code': 102, 'info': '无效的 yaml 格式配置文件'.format(yaml_error_info(str(e)))}
            self.__file_fp.close()
            # sys.exit(2)

    # def get_config_doc(self, doc_name: str = 'doc1') -> (dict, None):
    #     return self.yaml_config_data.get(doc_name)

    def get_status(self):
        return self.__fail
