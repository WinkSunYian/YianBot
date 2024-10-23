from nonebot import on_fullmatch
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    MessageSegment,
    PrivateMessageEvent,
)

from utils.utils import (
    DailyCountLimiter,
    BackpackControl
)
from utils.db_utils import UserBackpackManager

from random import choice

signin = on_fullmatch("#test", priority=6, block=True)


@signin.handle()
async def _(event: GroupMessageEvent):
    await signin.finish(MessageSegment.share("baidu.com") + "1")
