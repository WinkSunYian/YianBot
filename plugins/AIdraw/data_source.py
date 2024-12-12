import aiohttp
import json
from utils.http_utils import Aiohttp

async def get_draw_link(condition):
    async with aiohttp.ClientSession() as session:
        try:
            url = f"https://api.wer.plus/api/aiw?pra={condition}"
            resp = await session.get(url)
            data = json.loads(await resp.text())
            return data["url"]
        except:
            return "AI绘画超时"
