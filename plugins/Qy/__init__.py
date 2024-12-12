from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
    MessageSegment,
    Message
)
from nonebot.params import (
    CommandArg,
    Depends
)
import requests
from bs4 import BeautifulSoup

__plugin_name__ = 'Qy'
__plugin_usage__ = '缺氧'

draw = on_command("#缺氧论坛", aliases={"#论坛"}, priority=5, block=True)


@draw.handle()
async def draw_handle(event: MessageEvent):
    await draw.finish(MessageSegment.reply(event.message_id) + await a())


async def a():
    url = "http://154.44.10.128:1145/"
    response = requests.get(url, timeout=10)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, 'html.parser')
    list_ul = soup.find_all('ul', class_='list')
    list_li = list_ul[0].find_all("a")
    str = ""
    for i in list_li:
        text = i.text
        url = i.get("href")
        str += f"{text}{url}\n"

    return str
