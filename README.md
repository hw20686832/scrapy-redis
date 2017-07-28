# scrapy-redis
Redis based queue for Scrapy 

### INSTALL
1. Install pyreBloom
```shell
sudo apt-get install hiredis-dev
git clone https://github.com/seomoz/pyreBloom.git
cd pyreBloom
sudo python setup.py install
```
2. Install scrapy-redis
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
