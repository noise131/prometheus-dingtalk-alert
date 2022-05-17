def opts_help(exec_name):
    help_info = '''usage : {} [-hv] [-c YAML_CONFIG_PATH]'''.format(exec_name)
    print(help_info)


def opts_version(exec_name, version):
    print('{} : {}'.format(exec_name, version))
