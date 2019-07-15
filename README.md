# 架构图

![image](https://github.com/shiqinying/AdslProxy/raw/master/screenshots/adsl_proxy架构.jpg)

## 拨号主机设置

### 1.拨号上网
本教程以云立方vps ubuntu14为例
根据云主机拨号教程拨号上网，示例命令：

```
# 如果home文件夹里没有ppp.sh文件，证明已经安装好，可忽略
sh ppp.sh
#云立方默认配置.bashrc
# alias adsl-start=pppoe-start
# alias adsl-stop=pppoe-stop
adsl-start/adsl-stop 为自定义命令，为了避免python脚本执行shell命令错误
建议用pppoe-start，pppoe-stop原始命令

```

### 2.配置代理

以ubuntu上TinyProxy为例：

#### 安装

```
apt-get install -y epel-release
apt-get update -y
apt-get install -y tinyproxy
```

#### 配置

```
vi /etc/tinyproxy.conf
```

取消注释

```
Allow 127.0.0.1
```

#### 启动

```
云立方自带ubuntu系统不可用 systemctl命令
#systemctl enable tinyproxy.service
#systemctl restart  tinyproxy.service
可以使用
service tinyproxy restart

```

#### 测试

```
pppoe-start
ifconfig
# 代理ip地址在ppp0 网卡，tinyproxy默认端口 8888
curl -x IP:PORT www.baidu.com
```

IP为拨号主机IP，PORT为代理端口

#### 防火墙

如不能访问可能是防火墙问题，可以放行端口
云立方ubuntu14 默认没有开启防火墙，以下命令省略
```
iptables -I INPUT -p tcp --dport 8888 -j ACCEPT
```

或直接关闭防火墙

```
systemctl stop firewalld.service
```

### 3.安装Python3

#### CentOS

```
sudo yum groupinstall -y development tools
sudo yum install -y epel-release python34-devel  libxslt-devel libxml2-devel openssl-devel
sudo yum install -y python34 python34-setuptools
sudo easy_install-3.4 pip
```

#### Ubuntu
云立方ubuntu14 自带python3.4，可直接使用
需要安装 python3-pip

```
sudo apt-get install -y python3-dev build-essential libssl-dev libffi-dev libxml2 libxml2-dev libxslt1-dev zlib1g-dev
sudo apt-get install -y python3 python3-pip
```

### 4.安装库

vps 端不需要安装tornado，api服务器端都要安装

```
pip3 install redis tornado requests
```

### 5.Clone项目

```
apt-get install git
git clone https://github.com/shiqinying/AdslProxy.git
```

### 6.Redis

```
# vps 端只需要安装好即可，需要使用客户端连接远程redis服务
# api服务器端需要安装好后进行配置密码，开放端口等

apt-get install redis-server
```

Redis数据库可以配置在某台固定IP的VPS，也可以购买Redis独立服务，如阿里云、腾讯云等。
我这里同api接口配置在同一服务器

### 7.修改配置

配置文件是 adslproxy/config.py
```
cd /AdslProxy/adslproxy
vi config.py
```

根据注释修改配置文件，主要修改如下：

只需修改 CLIENT_NAME，REDIS_HOST，REDIS_PASSWORD三项

> #### ADSL_BASH
>
> 拨号命令，不同主机可能不同，默认 adsl-stop;adsl-start（不要用）
> 要用pppoe-start，pppoe-stop！！！
>
> #### PROXY_PORT
>
> 拨号主机代理端口，使用TinyProxy则默认为8888，使用Squid则默认3128，默认8888
>
> #### CLIENT_NAME
>
> 客户端唯一标识，不同拨号主机请设置不同的名称，默认adsl1
> 根据主机数量adsl1，adsl2，adsl3。。。
> #### ADSL_IFNAME 
>
> 拨号网卡名称，主要根据`ifconfig`命令获取拨号后该网卡的IP，默认ppp0
>
> #### REDIS_HOST
>
> Redis数据库地址，请修改为固定IP的Redis Host，注意保密
>
> #### REDIS_PASSWORD
>
> Redis数据库密码，如无则填None
>
> #### REDIS_PORT
>
> Redis数据库端口，默认6379
>
> #### PROXY_KEY
>
> Redis代理池键名开头，默认为adsl

### 8.运行

```
# adsl端
cd AdslProxy
python3 run.py
# api服务器端
cd AdslProxy
python3 api.py
```

守护运行（用supervisor取代）

```
(python3 run.py > /dev/null &)
(python3 api.py > /dev/null &)
```
使用supervisor管理进程

supervisor 是用python写的，可以通过pip 安装，目前只支持python2
虽然supervisor装在python2下，但是不要忘记运行时开启项目所需虚拟环境
```
pip2 install supervisor 
workon  <虚拟环境名称>
cd AdslProxy
#运行以下命令即可启动服务
# vps 
supervisord -c supervisor_adsl.conf
# 服务器api
supervisord -c supervisor_api.conf

```
以后要想管理 supervisor中的进程，可以通过以下命令进入supervisor控制台
```
#vps
supervisorctl -c supervisor_adsl.conf
#服务器api
supervisorctl -c supervisor_api.conf

status # 查看状态
start programe_name # 启动程序
restart programe_name # 重新启动程序
stop programe_name # 关闭程序
reload programe_name # 重新加载配置文件
quit # 退出控制台

```


## 程序使用

### 1.安装ADSLProxy

```
pip3 install adslproxy
```

### 2.Redis直连使用

```python
from adslproxy import RedisClient

client = RedisClient(host='', password='')
random = client.random()
all = client.all()
names = client.names()
proxies = client.proxies()
count = client.count()

print('RANDOM:', random)
print('ALL:', all)
print('NAMES:', names)
print('PROXIES:', proxies)
print('COUNT:', count)
```

参数说明如下：

> #### host
>
> 即Redis数据库IP
>
> #### password
>
> 即Redis数据库密码，没有则None
>
> #### port
>
> 即Redis数据库端口，默认6379
>
> #### proxy_key
>
> 即Redis数据库代理键名开头，默认adsl

方法说明如下：

> #### random()
>
> 从Redis代理池取随机代理
>
> #### all()
>
> 从Redis代理池取所有可用代理，返回list
>
> #### names()
>
> 从Redis代理池取主机列表
>
> #### proxies()
>
> 从Redis代理池取代理列表
>
> #### count()
>
> 从Redis代理池取所有可用主机数量

运行结果：

```python
RANDOM: 115.221.121.52:8888
ALL: {'adsl2': '118.119.111.172:8888', 'adsl3': '115.221.121.52:8888', 'adsl4': '58.22.111.23:8888', 'adsl1': '182.147.200.60:8888'}
NAMES: ['adsl2', 'adsl3', 'adsl4', 'adsl1']
PROXIES: ['118.119.111.172:8888', '115.221.121.52:8888', '58.22.111.23:8888', '182.147.200.60:8888']
COUNT: 4
```

代码使用：

```python
import requests
proxies  = {
  'http': 'http://' + client.random()
}
r = requests.get('http://httpbin.org/get', proxies=proxies)
print(r.text)
```

### 3.API使用

```python
from adslproxy import RedisClient, server
client = RedisClient(host='', password='', port='')
server(client, port=8000)
```

运行后会在8000端口监听，访问API即可取到相应代理

获取代理：

```python
import requests

def get_random_proxy():
    try:
        url = 'http://localhost:8000/random'
        return requests.get(url).text
    except requests.exceptions.ConnectionError:
        return None
```

代码使用：

```python
import requests
proxies  = {
  'http': 'http://' + get_random_proxy()
  'https': 'https://'+ get_random_proxy()
}
r = requests.get('http://httpbin.org/get', proxies=proxies)
print(r.text)
```