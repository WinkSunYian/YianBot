import aiohttp
import json


async def get_touch_link(user_id) -> str:
    async with aiohttp.ClientSession() as session:
        try:
            url = f"https://xiaoapi.cn/API/bq_mym.php?type=json&qq={user_id}"
            resp = await session.get(url)
            data = json.loads(await resp.text())
            return data["text"]
        except:
            return "摸不到"


async def get_pound_link(user_id) -> str:
    url = f"https://api.xingzhige.com/API/pound/?qq={user_id}"
    return url


async def get_bite_link(user_id) -> str:
    url = f"https://api.xingzhige.com/API/bite/?qq={user_id}"
    return url


async def get_misfortune_link(user_id) -> str:
    # 不幸
    url = f"https://api.andeer.top/API/un_for.php?qq={user_id}"
    return url


async def get_tietie_link(user_id) -> str:
    # 贴贴
    url = f"https://api.andeer.top/API/gif_tietie.php?qq={user_id}"
    return url


async def get_ding_link(user_id) -> str:
    # 顶
    url = f"https://api.xingzhige.com/API/dingqiu/?qq={user_id}"
    return url


async def get_luxun_link(text) -> str:
    # 鲁迅说
    url = f"https://api.andeer.top/API/img_luxun.php?text={text}"
    return url
