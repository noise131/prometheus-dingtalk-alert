import re


def get_yaml_doc(yaml_config_data: dict, doc_name: str) -> (dict, None):
    try:
        return yaml_config_data['{}'.format(doc_name)]
    except KeyError:
        print('yaml文件中没有文档 : %s' % doc_name)
        return None


def yaml_error_info(str1):
    str2 = ''
    for i in str1.split('\n'):
        str3, count = re.subn('^\s+', '', i)
        if count:
            str2 = '{}{}{}'.format(str2, str3, '; ')
        else:
            str2 = '{}{}{}'.format(str2, str3, ' ')
    return str2
