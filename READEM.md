## 简介

#####         这是一个高效易用的代理池的实现，旨在获取网上大量的免费代理中的有效代理。基本的模块分为4块：存储模块，获取模块，检测模块，接口模块。

### 存储模块

​        负责存储爬取的免费代理，去重，检测有效性，动态实时地处理每个代理，使用redis的有序集合

### 获取模块

​        定时在各大代理网站爬取代理，抓取到的有效代理将被存到数据库中

### 检测模块

​        定时检测数据库中的代理，设置代理权重，每次检测可用则权重为100，若，代理不可用，则置为低权重，每次检测失败则权重减一，直至从数据库中移除

### 接口模式

​        利用flask设置一个web API接口，通过访问接口拿到可用代理，安全方便，如果不想用接口，也可以直接连接数据库获取：



import requests

PROXY_POOL_URL = 'http://localhost:5555/random'

def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None



参考地址：https://cuiqingcai.com/

