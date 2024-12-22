from nonebot import on_fullmatch
from nonebot.adapters.onebot.v11 import Bot, MessageSegment, MessageEvent

from utils.utils import args_split, ConfigReader
import os

help = on_fullmatch("菜单", priority=5, block=True)


@help.handle()
async def _(event: MessageEvent):
    msg_list = [
        "今日运势",
        "签到",
        "#背包",
        "打劫",
        "摸",
    ]

    await help.finish(MessageSegment.reply(event.message_id) + "\n".join(msg_list))
