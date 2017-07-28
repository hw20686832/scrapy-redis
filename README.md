# scrapy-redis
Redis based queue for Scrapy 

### INSTALL
```shell
git clone https://github.com/hw20686832/scrapy-redis.git
cd scrapy-redis
sudo python setup.py install
```

### USAGE
  Add following code in settings.py
  ```python
  DUPEFILTER_CLASS = "scrapy_redis.extensions.duperfilter.RFPDupeFilter"
  SCHEDULER = "scrapy_redis.scheduler.Scheduler"

  REDIS_CONF = {
      'host': 'localhost',
      'port': 6379,
      'db': 10
  }
  ```
