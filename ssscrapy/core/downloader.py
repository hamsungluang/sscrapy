import asyncio

import requests


class Downloader:

    def __init__(self):
        self._active = set()

    async def fetch(self, request):
        self._active.add(request)
        response = await self.download(request)
        self._active.remove(request)
        return response

    async def download(self, request):
        # resp = requests.get(request.url)
        # print(resp.status_code)
        await asyncio.sleep(1)
        return 'result'

    def __len__(self):
        return len(self._active)

    def idle(self) -> bool:
        return len(self) == 0
