from ssscrapy import Request
from ssscrapy.spider import Spider


class BaiduSpider(Spider):
    start_urls = ["https://www.baidu.com", "https://www.baidu.com"]
    custom_settings = {"CONCURRENCY": 8}

    def parse(self, response):
        print('parse', response)
        for i in range(10):
            url = "https://www.baidu.com"
            yield Request(url, callback=self.parse_page)

    def parse_page(self, response):
        print('parse_page', response)
        for i in range(10):
            url = "https://www.baidu.com"
            yield Request(url, callback=self.parse_detail)

    def parse_detail(self, response):
        print('parse_detail', response)
