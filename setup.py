from setuptools import setup, find_packages


setup(
    name='scrapy-redis',
    packages=find_packages(),
    version='0.1.0',
    description='Redis based queue for Scrapy',
    author='David Wong',
    author_email='stef-hw@163.com',
    url='https://github.com/hw20686832/scrapy-redis',
    download_url='https://github.com/hw20686832/scrapy-redis/archive/v0.1.tar.gz',
    keywords=['scrapy', 'redis'],
    install_requires=['redis'],
    classifiers=[],
)
