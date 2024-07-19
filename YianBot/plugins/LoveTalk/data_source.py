import aiohttp
import requests


async def get_love_talk():
    url = f"https://api.mcloc.cn/love/"
    data = requests.get(url).text
    return data
