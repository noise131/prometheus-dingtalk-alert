import sys
import getopt
# from globalConfig import *
# import globalConfig
from .optsFunction import *

OPTS_YAML_CONFIG_FILE = 'config.yaml'
MAIN_VERSION: str = '1.0'
EXEC_NAME: str = 'main.py'

try:
    opts, other_args = getopt.getopt(sys.argv[1:], 'hvc:', ['help', 'version', 'config'])
except getopt.GetoptError as e:
    r = str(e).split()
    print('[ERROR] Unknown option : \'%s\'' % (r[1]))
    sys.exit(1)
if other_args:
    print('[ERROR] Parameters that should not appear : \'%s\'' % (other_args[0]))
    sys.exit(1)

for o, a in opts:
    if o in ('-h', '--help'):
        opts_help(EXEC_NAME)
        sys.exit(0)
    elif o in ('-v', '--version'):
        opts_version(EXEC_NAME, MAIN_VERSION)
        sys.exit(0)
    elif o in ('-c', '--config'):
        OPTS_YAML_CONFIG_FILE = a