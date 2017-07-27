# coding:utf-8
import redis


class RedisQueue(object):
    def __init__(self, settings):
        self.redis = redis.Redis(**settings.get('REDIS_CONF'))
        self.queue_key = settings.get('QUEUE_KEY', 'scrapy:queue')

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    def get(self):
        return self.redis.lpop(self.queue_key)

    def put(self, seed):
        return self.redis.rpush(self.queue_key, seed)

    def __len__(self):
        return self.redis.llen(self.queue_key)

    def flush(self):
        self.redis.delete(self.queue_key)
