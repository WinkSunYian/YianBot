import aiohttp
import json
import requests
from configs.configs import BaiduCloudConfig


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": BaiduCloudConfig.baidu_api_key,
              "client_secret": BaiduCloudConfig.baidu_secret_key}

    return str(requests.post(url, params=params).json().get("access_token"))


token = get_access_token()


async def text_review(message: str) -> json:
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    payload = f"text={message}"
    async with aiohttp.ClientSession(headers=headers) as session:
        try:
            url = "https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined?access_token=" + token
            async with session.request(url=url, method='POST', data=payload, verify_ssl=False) as response:
                data = json.loads(await response.text())
                return data
        except TimeoutError:
            return json.loads('{"conclusion": "合规"}')
