# coding:utf-8
import json
import pickle

from scrapy.utils.reqser import request_to_dict, request_from_dict
from scrapy.utils.misc import load_object

from .queue import PriorityQueue


class ScrapyRequestEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            data = {}
            data['id'] = id(obj)
            data['obj'] = pickle.dumps(obj)
            data['__type__'] = "__scrapy_obj__"
        except:
            return json.JSONEncoder.default(self, obj)

        return data


def scrapy_request_decoder(obj):
    if '__type__' in obj:
        if obj.pop('__type__') == '__scrapy_obj__':
            obj = pickle.loads(obj['obj'])

    return obj


class Scheduler(object):
    """Redis-based scheduler"""
    def __init__(self, dupefilter, queue, stats=None, settings=None):
        self.df = dupefilter
        self.queue = queue
        self.stats = stats
        self.settings = settings

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        dupefilter_cls = load_object(settings['DUPEFILTER_CLASS'])
        dupefilter = dupefilter_cls.from_settings(settings)
        queue = PriorityQueue.from_settings(settings)
        return cls(dupefilter, queue, crawler.stats, settings)

    def has_pending_requests(self):
        return len(self) > 0

    def open(self, spider):
        self.spider = spider
        return self.df.open(spider)

    def close(self, reason):
        self.queue.flush()
        return self.df.close(reason)

    def enqueue_request(self, request):
        if not request.dont_filter and self.df.request_seen(request):
            self.df.log(request, self.spider)
            return

        self._eqpush(request)
        self.stats.inc_value('scheduler/enqueued/redis', spider=self.spider)

    def next_request(self):
        request = self._dqpop()
        if request:
            self.stats.inc_value('scheduler/dequeued/redis', spider=self.spider)
        return request

    def __len__(self):
        return len(self.queue)

    def _eqpush(self, request):
        req_dict = request_to_dict(request, self.spider)
        req = json.dumps(req_dict, cls=ScrapyRequestEncoder)
        self.queue.put(req, request.priority)

    def _dqpop(self):
        if self.queue:
            d = self.queue.get()
            if d:
                return request_from_dict(
                    json.loads(d, object_hook=scrapy_request_decoder),
                    self.spider
                )
