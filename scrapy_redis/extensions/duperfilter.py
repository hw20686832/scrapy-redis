# coding:utf-8
import logging
from hashlib import md5

import pyreBloom
from scrapy.dupefilters import BaseDupeFilter


class RFPDupeFilter(BaseDupeFilter):
    """Request Fingerprint duplicates filter"""
    def __init__(self, settings):
        self.logger = logging.getLogger('Dupefilter')
        redis_conf = settings.get("REDIS_CONF")
        self.urls_seen = pyreBloom.pyreBloom(
            "bfilter:{}".format(settings.get('TASK_ID')),
            100000000, 0.001,
            host=redis_conf['host'],
            port=redis_conf['port'],
            db=redis_conf['db']
        )

        self.logdupes = True

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    def request_seen(self, request):
        _uid = md5(request.url).hexdigest()
        if _uid in self.urls_seen:
            return True

    def close(self, reason):
        self.urls_seen.delete()

    def log(self, request, spider):
        if self.logdupes:
            fmt = "Filtered duplicate request: %(request)s - no more duplicates will be shown (see DUPEFILTER_CLASS)"
            self.logger.debug(fmt % {"request": request, "spider": spider})
            self.logdupes = False
