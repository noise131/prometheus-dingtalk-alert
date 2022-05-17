from setuptools import setup, find_packages

setup(name='DingtalkRobot',
      version='0.0.1',
      description='optsHandle',
      url='noise131.com',
      author='noise131',
      author_email='optsHandle@163.com',
      requires=['json', 'random', 'typing', 'requests', 'time', 'hmac', 'hashlib', 'base64', 'urllib'],  # 定义依赖哪些模块
      packages=find_packages(),  # 系统自动从当前目录开始找包
      # packages=['__init__', 'dingtalkRobot', 'messageTools', 'signTools'],
      license="apache 3.0",
      zip_safe=False,
      gzip=False
      )
