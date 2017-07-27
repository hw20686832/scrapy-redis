# coding:utf-8
import logging
from hashlib import md5

import pyreBloom
from scrapy.dupefilters import BaseDupeFilter


class RFPDupeFilter(BaseDupeFilter):
    """Request Fingerprint duplicates filter"""
    def __init__(self, settings):
        self.logger = logging.getLogger('Dupefilter')
        self.settings = settings
        self.urls_seen = None
        self.logdupes = True

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    def open(self, spider):
        redis_conf = self.settings.get("REDIS_CONF")
        self.urls_seen = pyreBloom.pyreBloom(
            "bfilter:{}".format(spider.name),
            100000000, 0.001,
            host=redis_conf['host'],
            port=redis_conf['port'],
            db=redis_conf['db']
        )

    def request_seen(self, request):
        _uid = md5(request.url).hexdigest()
        if _uid in self.urls_seen:
            return True

        self.urls_seen.add(_uid)

    def close(self, reason):
        if self.urls_seen:
            self.urls_seen.delete()

    def log(self, request, spider):
        if self.logdupes:
            fmt = "Filtered duplicate request: %(request)s - no more duplicates will be shown (see DUPEFILTER_CLASS)"
            self.logger.debug(fmt % {"request": request, "spider": spider})
            self.logdupes = False
