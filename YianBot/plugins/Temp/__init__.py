from nonebot import on_command
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent
)

from utils.utils import ConfigurationControl, DailyCountLimiter
import asyncio
from random import randint

__plugin_name__ = "Temp"

# config = ConfigurationControl("plugins/" + __plugin_name__ + "/config.json")


signin = on_command("#哈", priority=6, block=True)


@signin.handle()
async def signin_handle(bot: Bot, event: GroupMessageEvent):
    while True:
        await asyncio.sleep(randint(30, 60))
        await bot.send_msg(
            message_type="private",
            # 私聊用户QQ号
            user_id=2074731829,
            message='哄不好'
        )


