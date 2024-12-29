from nonebot import on_fullmatch
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    MessageSegment,
    PrivateMessageEvent,
)

from utils.utils import DailyCountLimiter, BackpackControl
from pathlib import Path
from random import choice

signin = on_fullmatch("#test", priority=6, block=True)


@signin.handle()
async def _(event: GroupMessageEvent):
    path = Path("/data/YianBot/data/oxygen_card/fieldset_screenshot.png")
    if not path.exists():
        print(f"文件不存在: {path}")
    else:
        print(f"文件存在: {path}")

    with open(path, "rb") as f:
        image_bytes = f.read()
    await signin.finish(MessageSegment.image(image_bytes))
