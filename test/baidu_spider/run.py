import asyncio
import time

from ssscrapy.core.engine import Engine
from test.baidu_spider.spiders.baidu import BaiduSpider
from ssscrapy.utils.project import get_settings
from ssscrapy.crawler import CrawlerProcess


async def run():
    settings = get_settings('settings')
    process = CrawlerProcess(settings)
    baidu_spider = BaiduSpider()
    engine = Engine(settings)
    await engine.start_spider(baidu_spider)

if __name__ == '__main__':
    t = time.time()
    asyncio.run(run())
    print(time.time() - t)
