# encoding: utf-8

import datetime


def now_time_format():
    date = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    return date


#
# if __name__ == '__main__':
#     pass
