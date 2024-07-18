import asyncio
import time

from ssscrapy.core.engine import Engine
from test.baidu_spider.spiders.baidu import BaiduSpider
from test.baidu_spider.spiders.baidu2 import BaiduSpider2
from ssscrapy.utils.project import get_settings
from ssscrapy.crawler import CrawlerProcess


async def run():
    settings = get_settings('settings')
    process = CrawlerProcess(settings)
    await process.crawl(BaiduSpider)
    await process.crawl(BaiduSpider2)
    await process.start()

if __name__ == '__main__':
    t = time.time()
    asyncio.run(run())
    print(time.time() - t)
