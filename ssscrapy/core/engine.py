import asyncio
from typing import Optional, Generator, Callable
from inspect import iscoroutine

from ssscrapy import Request
from ssscrapy.core.downloader import Downloader
from ssscrapy.core.scheduler import Scheduler
from ssscrapy.exceptions import OutputError
from ssscrapy.spider import Spider
from ssscrapy.utils.spider import transform
from ssscrapy.task_manager import TaskManager


class Engine:

    def __init__(self, settings):
        self.downloader: Optional[Downloader] = None
        self.scheduler: Optional[Scheduler] = None
        self.spider: Optional[Spider] = None
        self.start_requests: Optional[Generator] = None
        self.task_manager: TaskManager = TaskManager(settings.getint('CONCURRENCY'))
        self.running = False

    async def start_spider(self, spider):
        self.running = True
        self.spider = spider
        self.scheduler = Scheduler()
        self.scheduler.open()
        self.start_requests = iter(spider.start_requests())
        self.downloader = Downloader()
        await self._open_spider()

    async def _open_spider(self):
        crawling = asyncio.create_task(self.crawl())
        # 这里可以做其他事情
        await crawling

    async def crawl(self):
        """主逻辑"""
        while self.running:
            if (request := await self._get_next_request()) is not None:
                await self._crawl(request)
            else:
                try:
                    start_request = next(self.start_requests)
                except StopIteration:
                    self.start_requests = None
                except Exception as e:
                    # 发起请求的task要运行完毕
                    # 调度器是否空闲
                    # 下载器是否空闲
                    if not await self._exit():
                        continue
                    self.running = False
                else:
                    # 入队
                    await self.enqueue_request(start_request)

    async def _crawl(self, request):
        # todo 实现并发
        async def crawl_task():
            outputs = await self._fetch(request)
            # 处理outputs
            if outputs:
                await self._handle_spider_output(outputs)

        # asyncio.create_task(crawl_task())
        await self.task_manager.semaphore.acquire()
        self.task_manager.create_task(crawl_task())

    async def _fetch(self, request):
        async def _success(_response):
            callback: Callable = request.callback or self.spider.parse
            if _outputs := callback(_response):
                if iscoroutine(_outputs):
                    await _outputs
                else:
                    return transform(_outputs)

        _response = await self.downloader.fetch(request)
        outputs = await _success(_response)
        return outputs

    async def enqueue_request(self, request):
        await self._schdule_request(request)

    async def _schdule_request(self, request):
        # todo 去重
        await self.scheduler.enqueue_request(request)

    async def _get_next_request(self):
        return await self.scheduler.next_request()

    async def _handle_spider_output(self, outputs):
        async for spider_output in outputs:
            if isinstance(spider_output, Request):
                await self.enqueue_request(spider_output)
            # todo 需要判断是否数据
            else:
                raise OutputError(f"{type(self.spider)} must return `Request` or `Item`")

    async def _exit(self):
        if self.scheduler.idle() and self.downloader.idle() and self.task_manager.all_done():
            return True
        return False
