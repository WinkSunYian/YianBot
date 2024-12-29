from nonebot import on_fullmatch
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    MessageSegment,
    PrivateMessageEvent,
)

from utils.utils import DailyCountLimiter, BackpackControl

from random import choice

signin = on_fullmatch("#test", priority=6, block=True)


@signin.handle()
async def _(event: GroupMessageEvent):
    import os
    if not os.path.exists(path):
        print("文件不存在:", path)
    else:
        print("文件存在:", path)
    path = "/data/YianBot/data/oxygen_card/fieldset_screenshot.png"
    await signin.finish(MessageSegment.image(path))
