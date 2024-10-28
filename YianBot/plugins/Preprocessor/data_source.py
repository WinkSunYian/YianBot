# from utils.http_utils import Aiohttp
import aiohttp


async def get_user_tags(user_id: int) -> list:
    url = "http://bot.sunyian.cloud/api/users/{user_id}/tags"
    headers = {"app-key": "QMCjya2bw60Fh4BMDshA5iQbcZI3l3GM"}
    response = await Aiohttp(url, method="GET", headers=headers)
    return response


def is_tag_present(tag_list: list, tag_name: str) -> bool:
    for tag in tag_list:
        if tag.get("tag_name") == tag_name:
            return True
    return False


async def Aiohttp(
    url, method="GET", headers=None, data=None, verify=True, timeout=10
) -> str:
    async with aiohttp.ClientSession() as session:
        try:
            if method.upper() == "POST":
                resp = await session.post(
                    url, headers=headers, data=data, verify_ssl=verify, timeout=timeout
                )
            else:
                resp = await session.get(
                    url, headers=headers, data=data, verify_ssl=verify, timeout=timeout
                )
            text = await resp.text()
            return text
        except:
            return ""


# 发起一个异步请求
if __name__ == "__main__":
    import asyncio

    a = asyncio.run(get_user_tags(10086))
    print(a)
