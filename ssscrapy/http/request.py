from typing import Dict, Optional, Callable


class Request:

    def __init__(
            self,
            url: str,
            *,
            headers: Optional[Dict] = None,
            callback: Optional[Callable] = None,
            priority: int = 1,
            method: str = 'GET',
            cookies: Optional[Dict] = None,
            proxy: Optional[Dict] = None,
    ):
        self.url = url
        self.headers = headers
        self.priority = priority
        self.method = method
        self.cookies = cookies
        self.proxy = proxy
        self.callback = callback

    def __lt__(self, other):
        return self.priority < other.priority
