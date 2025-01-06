import aiohttp


class HTTPClient:
    def __init__(self, base_url=None, headers=None):
        self.base_url = base_url or ""
        self.headers = headers or {}

    async def get(self, endpoint, params=None, headers=None):
        url = self.base_url + endpoint
        headers = headers or self.headers
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, params=params, headers=headers) as response:
                return response.status, await response.json()

    async def post(self, endpoint, data=None, json=None, headers=None):
        url = self.base_url + endpoint
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(
                url, data=data, json=json, headers=headers
            ) as response:
                return response.status, await response.json()

    async def put(self, endpoint, data=None, json=None, headers=None):
        url = self.base_url + endpoint
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.put(
                url, data=data, json=json, headers=headers
            ) as response:
                return response.status, await response.json()

    async def delete(self, endpoint, headers=None):
        url = self.base_url + endpoint
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.delete(url, headers=headers) as response:
                return response.status, await response.json()


http_client = HTTPClient(
    base_url="http://bot.sunyian.cloud/api",
    headers={"app-key": "QMCjya2bw60Fh4BMDshA5iQbcZI3l3GM"},
)
