import aiohttp


class HTTPClient:
    def __init__(self, base_url=None, headers=None):
        """
        初始化 HTTP 客户端。

        :param base_url: 基础 URL（可选）
        :param headers: 默认请求头（可选）
        """
        self.base_url = base_url or ""
        self.headers = headers or {}

    async def get(self, endpoint, params=None, headers=None):
        """
        发送 GET 请求。

        :param endpoint: 请求的 API 地址
        :param params: 查询参数
        :param headers: 请求头
        :return: 响应状态码和数据
        """
        url = self.base_url + endpoint
        # 合并默认头部和传入的头部
        headers = headers or self.headers

        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, params=params, headers=headers) as response:
                # 如果返回的不是 JSON 格式，使用 .text() 解析 HTML 或其他类型的响应
                if response.status == 200:
                    if "application/json" in response.headers.get("Content-Type", ""):
                        try:
                            data = await response.json()
                        except aiohttp.ContentTypeError:
                            # 如果解析失败，返回错误信息
                            data = {"error": "Failed to decode JSON"}
                    else:
                        # 如果不是 JSON 格式，返回响应的文本内容
                        data = await response.text()
                else:
                    # 处理非 200 状态码
                    data = {"error": f"Request failed with status {response.status}"}

                return response.status, data

    async def post(self, endpoint, data=None, json=None, headers=None):
        """
        发送 POST 请求。

        :param endpoint: 请求的 API 地址
        :param data: 表单数据
        :param json: JSON 数据
        :param headers: 请求头
        :return: 响应状态码和数据
        """
        url = self.base_url + endpoint
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.post(
                url, data=data, json=json, headers=headers
            ) as response:
                data = await response.json()
                return response.status, data

    async def put(self, endpoint, data=None, json=None, headers=None):
        """
        发送 PUT 请求。

        :param endpoint: 请求的 API 地址
        :param data: 表单数据
        :param json: JSON 数据
        :param headers: 请求头
        :return: 响应状态码和数据
        """
        url = self.base_url + endpoint
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.put(
                url, data=data, json=json, headers=headers
            ) as response:
                data = await response.json()
                return response.status, data

    async def delete(self, endpoint, headers=None):
        """
        发送 DELETE 请求。

        :param endpoint: 请求的 API 地址
        :param headers: 请求头
        :return: 响应状态码和数据
        """
        url = self.base_url + endpoint
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.delete(url, headers=headers) as response:
                data = await response.json()
                return response.status, data


http_client = HTTPClient(
    base_url="http://bot.sunyian.cloud/api",
    # base_url="http://127.0.0.1:80/yianbot/api",
    headers={"app-key": "QMCjya2bw60Fh4BMDshA5iQbcZI3l3GM"},
)


async def TEST(user_id, q):
    status, response = await http_client.put(f"/users/{user_id}/sign-in")
    print(response)


if __name__ == "__main__":
    import asyncio

    async def main():
        inputText = "7345222"
        user_id = "7345222"
        response = await TEST(inputText, user_id)

    asyncio.run(main())
