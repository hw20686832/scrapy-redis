# coding:utf-8
import redis


class RedisQueue(object):
    def __init__(self, rd, queue_key=None):
        self.redis = rd
        self.queue_key = queue_key

    @classmethod
    def from_settings(cls, settings):
        rd = redis.Redis(**settings.get('REDIS_CONF'))
        queue_key = settings.get('QUEUE_KEY', 'scrapy:queue')
        return cls(rd, queue_key)

    def get(self):
        raise NotImplementedError()

    def put(self, seed):
        raise NotImplementedError()

    def flush(self):
        self.redis.delete(self.queue_key)


class FifoQueue(RedisQueue):
    def get(self):
        return self.redis.lpop(self.queue_key)

    def put(self, seed):
        return self.redis.rpush(self.queue_key, seed)

    def __len__(self):
        return self.redis.llen(self.queue_key)


class PriorityQueue(RedisQueue):
    def get(self):
        last_item = self.redis.zrange(self.queue_key, -1, -1)
        if last_item:
            self.redis.zrem(self.queue_key, last_item[0])
            return last_item[0]

    def put(self, seed, priority=0):
        self.redis.zadd(self.queue_key, seed, priority)

    def __len__(self):
        return self.redis.zcard(self.queue_key)
