import sys

import globalConfig
import pda_webhook_flsk

if __name__ == '__main__':
    # 运行 pda_webhook_flsk webhook
    try:
        pda_webhook_flsk.webhook_app.run(host=globalConfig.CONFIG_WEBHOOK_HOST, port=int(globalConfig.CONFIG_WEBHOOK_PORT))
    except (Exception, OSError) as e:
        print('启动失败，错误信息 : {}'.format(str(e)))
