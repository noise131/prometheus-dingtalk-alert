# prometheus-dingtalk-alter

prometheus(alertmanager) 钉钉告警模块

# 基本环境

### 测试环境相关软件版本

测试使用相关程序的版本为

- python : **3.6.10**
- prometheus : **2.35.0**
- alertmanager : **0.24.0**

以上环境测试功能全部正常

### python 需要安装的软件包

```shell
]# pip install pyyaml \
               flask \
               requests
```


# 基本用法

Usage : python3  main.py  [-hv]  [-c CONFIG_FILE]

- -h : 获取使用帮助
- -v : 获取软件版本号
- -c CONFIG_FILE | --config CONFIG_FILE : 指定配置文件位置

  - default : ./config.yaml

# 配置文件

默认配置文件 ./config.yaml

默认配置内容

```yaml
---
# 模板文件位置，默认模板为 markdown 格式模板, 如果需要是同 text 类型只需要将 markdown 相关语法字符删除即可
template: ./templates/default_dingtalk-templates.tmpl

# 钉钉机器人的配置
dingtalkRobotConfig:
  # 每个机器人配置为一个列表, robot 键指定机器人名, 机器人名在进行 alertmanager 调用时需要用到
  - robot: robot-1
    webhook: https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxx
    # 指定机器人的安全类型
    # keyword : 关键字, value 键值应该配置为列表, 列表中为一个或多个关键字
    # secret : 加签, value 键值应为机器人的加签密钥内容
    securityType:
      type: keyword
      value:
        - test
        - abc
  - robot: robot-2
    webhook: https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxx
    securityType:
      type: secret
      value: SECce56667cfxxxxxxxxxxxxxxxxxx4b5d500f31fe67f
    # 该机器人所发送消息的类型, 默认为 text 类型
    messageType: markdown
    # 发送消息 @ 指定人的手机号列表，默认为空列表，即不 @ 任何人
    atMobiles:
      - '156xxxxx405'
    # 是否 @ 所有人, 默认即为 false
    atAll: false

# webhook 监听配置
webhookListen:
  # 监听地址
  host: 0.0.0.0
  # 监听端口
  port: 8000
```

# alertmanager 配置

```yaml
......
route:
  # server 为本人自定义的标签
  group_by: ['alertname','server']
  group_wait: 30s
  group_interval: 10s
  repeat_interval: 12h
  receiver: 'webhook-dingtalk'
......
receivers:
- name: 'webhook-dingtalk'
  webhook_configs:
  # webhook 接收器 url 配置为该程序的接口地址，其中 robot-2 是 config.yaml 中的机器人名，其余 uri 为固定格式
  - url: 'http://172.5.1.100:8000/webhook/robot-2/send'
    send_resolved: true
......
```

# 默认模板

```jinjia2
{# prometheus webhook json 已拆分 alters 列表将内部的每个字典单独传递到模板，#}
{# 模板调用顶层参数只需要写 alters 列表中字典的键即可。webhook json 数据详细信息见下文 #}

{# 如果是告警内容使用以下模板 #}
{% if status == 'firing' %}
## **<font color="#FF0000">告警简要</font>**
- 告警名 : {{labels.alertname}}
- 告警值 : {{annotations.value}}
- 严重性 : {{labels.severity}}
- 告警主机 : {{labels.server}}
- 告警时间 : {{startsAt}}
- 告警描述 : {{annotations.description}}
## **Labels List**
{% for label_k, label_v in labels.items() %}
> {{label_k}} : {{label_v}}
{% endfor %}
{% endif %}

{# 如果使恢复内容使用以下模板 #}
{% if status == 'resolved' %}
## **<font color="#4CC417">恢复简要</font>**
- 告警名 : {{labels.alertname}}
- 严重性 : {{labels.severity}}
- 告警主机 : {{labels.server}}
- 告警时间 : {{startsAt}}
- <font color="#4CC417">恢复时间</font> : {{endsAt}}
- 告警描述 : {{annotations.description}}
## **Labels List**
{% for label_k, label_v in labels.items() %}
> {{label_k}} : {{label_v}}
{% endfor %}
{% endif %}
```

# prometheus webhook json 数据示例

prometheus webhook 实际上就是通过 POST 请求提交 JSON 格式数据到指定接口

### 告警的 json 数据

```
{
    'receiver': 'webhook-zdy',
    'status': 'firing',
    'alerts': [
        {
            'status': 'firing',
            'labels': {
                'alertname': 'Memoryusagegreaterthan70%',
                'inhibit_info': 'memusagehigh',
                'instance': '172.5.1.100: 9100',
                'job': 'node_exporter',
                'server': 'docker-01',
                'severity': 'warning'
            },
            'annotations': {
                'description': '内存使用率持续5m大于70%',
                'title': 'Memoryusagehigh',
                'value': '76%'
            },
            'startsAt': '2022-05-15T11: 06: 29.14Z',
            'endsAt': '0001-01-01T00: 00: 00Z',
            'generatorURL': 'http: //prometheus-01: 9090/graph?g0.expr=ceil%28%28%28node_memory_MemTotal_bytes+-+node_memory_MemAvailable_bytes%29+%2F+node_memory_MemTotal_bytes+%2A+100%29%29+%3E+70&g0.tab=1',
            'fingerprint': 'b1d911e070fe50ea'
        }
    ],
    'groupLabels': {
        'alertname': 'Memoryusagegreaterthan70%',
        'server': 'docker-01'
    },
    'commonLabels': {
        'alertname': 'Memoryusagegreaterthan70%',
        'inhibit_info': 'memusagehigh',
        'instance': '172.5.1.100: 9100',
        'job': 'node_exporter',
        'server': 'docker-01',
        'severity': 'warning'
    },
    'commonAnnotations': {
        'description': '内存使用率持续5m大于70%',
        'title': 'Memoryusagehigh',
        'value': '76%'
    },
    'externalURL': 'http: //prometheus-01: 9093',
    'version': '4',
    'groupKey': '{
        
    }/{
        severity="warning"
    }: {
        alertname="Memory usage greater than 70%",
        server="docker-01"
    }',
    'truncatedAlerts': 0
}
```

### 恢复告警的 json 数据

```
{
    'receiver': 'webhook-zdy',
    'status': 'resolved',
    'alerts': [
        {
            'status': 'resolved',
            'labels': {
                'alertname': 'Instancedown',
                'inhibit_info': 'instancedown',
                'instance': '172.5.1.7: 9100',
                'job': 'node_exporter',
                'server': 'web-nginx-01',
                'severity': 'disastrous'
            },
            'annotations': {
                'description': 'Instanceup{
                    
                }指标值连续1分钟为0,
                判定为掉线',
                'title': 'Instancedown',
                'value': '0'
            },
            'startsAt': '2022-05-16T15: 12: 15.673Z',
            'endsAt': '2022-05-16T15: 13: 30.673Z',
            'generatorURL': 'http: //prometheus-01: 9090/graph?g0.expr=up+%3D%3D+0&g0.tab=1',
            'fingerprint': '9300e76106b27287'
        }
    ],
    'groupLabels': {
        'alertname': 'Instancedown',
        'server': 'web-nginx-01'
    },
    'commonLabels': {
        'alertname': 'Instancedown',
        'inhibit_info': 'instancedown',
        'instance': '172.5.1.7: 9100',
        'job': 'node_exporter',
        'server': 'web-nginx-01',
        'severity': 'disastrous'
    },
    'commonAnnotations': {
        'description': 'Instanceup{
            
        }指标值连续1分钟为0,
        判定为掉线',
        'title': 'Instancedown',
        'value': '0'
    },
    'externalURL': 'http: //prometheus-01: 9093',
    'version': '4',
    'groupKey': '{
        
    }/{
        severity=~"^(?:disastrous|critical)$"
    }: {
        alertname="Instance down",
        server="web-nginx-01"
    }',
    'truncatedAlerts': 0
}
```

# 告警信息效果示例

### 告警信息效果

![告警信息效果](https://github.com/noise131/ResourceRepo/blob/main/prometheus-dingtalk-alert/firing_message.png?raw=true)

### 恢复信息效果

![恢复信息效果](https://github.com/noise131/ResourceRepo/blob/main/prometheus-dingtalk-alert/resolved_message.png?raw=true)



