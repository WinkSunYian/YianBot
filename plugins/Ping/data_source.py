import aiohttp


async def get_ping(website):
    url = f"https://xiaoapi.cn/API/sping.php?url={website}"
    data = requests.get(url).text
    data = data.replace("：", ": ")
    return data
