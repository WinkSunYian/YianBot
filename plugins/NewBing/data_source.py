from utils.http_utils import Aiohttp
import json


async def get_chatgpt_answer(q):
    url = f"http://ovoa.cc/api/Bing.php?msg={q}"
    data = await Aiohttp(url)
    data = json.loads(data)["content"]
    return data
