import redis
from proxypool.error import PoolEmptyError
from proxypool.setting import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_KEY
from proxypool.setting import MAX_SCORE, MIN_SCORE, INITIAL_SCORE
from random import choice
import re


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    # 添加代理，权重置为最高
    def add(self, proxy, score=INITIAL_SCORE):
        if not re.match('\d+\.\d+\.\d+\.\d+\:\d+', proxy):
            print('代理不符合规范', proxy, '丢弃')
            return
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY, score, proxy)

    # 随机获取代理池中代理
    def random(self):
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        # 获取最高权重代理
        if len(result):
            return choice(result)
        # 按排名获取
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 100)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError

    # 代理权重减一
    def decrease(self, proxy):
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前权重', score, '减1')
            return self.db.zincrby(REDIS_KEY, proxy, -1)
        # 如果权重小于最小值，则剔除
        else:
            print('代理', proxy, '当前权重', score, '移除')
            return self.db.zrem(REDIS_KEY, proxy)

    # 判断代理是否已经存在
    def exists(self, proxy):
        return not self.db.zscore(REDIS_KEY, proxy) == None

    #将代理权重设置为最高
    def max(self, proxy):
        print('代理', proxy, '可用，设置为', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    # 代理数量
    def count(self):
        return self.db.zcard(REDIS_KEY)

    # 获取全部代理
    def all(self):
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    # 批量获取代理
    def batch(self, start, stop):
        return self.db.zrevrange(REDIS_KEY, start, stop - 1)


if __name__ == '__main__':
    conn = RedisClient()
    result = conn.batch(680, 688)
    print(result)