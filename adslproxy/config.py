# coding=utf-8
# 拨号间隔
ADSL_CYCLE = 120

# 拨号出错重试间隔
ADSL_ERROR_CYCLE = 1

# 删除代理到重新获取代理间隔
DEL_TO_GET = 5

# ADSL命令,adsl-stop;adsl-start 是.bashrc
# alias adsl-start=pppoe-start
# alias adsl-stop=pppoe-stop
#在 subprocess.getstatusoutput(ADSL_BASH) 会发生错误，只能执行/bin/sh 中的命令
ADSL_BASH = 'pppoe-stop;pppoe-start'

# 代理运行端口
PROXY_PORT = 8888

# 客户端唯一标识
CLIENT_NAME = 'adsl1'

# 拨号网卡
ADSL_IFNAME = 'ppp0'

# Redis数据库IP
REDIS_HOST = ''

# Redis数据库密码, 如无则填None
REDIS_PASSWORD = ''

# Redis数据库端口
REDIS_PORT = 6379

# 代理池键名
PROXY_KEY = 'adsl'

# 测试URL
TEST_URL = 'http://www.baidu.com'

# 测试超时时间
TEST_TIMEOUT = 2

# API端口
API_PORT = 8000
