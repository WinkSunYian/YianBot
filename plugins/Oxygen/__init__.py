from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment, Message
from nonebot.params import CommandArg, Depends
from .data_source import get_oxygen_card
from utils.utils import UserBlockLimiter
from dependencies.get_args_list import get_args_list
import json


user_block_limiter = UserBlockLimiter()

with open(".缺氧数据库.json", "r", encoding="utf-8") as f:
    data = json.load(f)

qy = on_command("#缺氧", aliases={"缺氧"}, priority=5, block=True)


@qy.handle()
async def _(
    bot: Bot,
    event: MessageEvent,
    args_list: list = Depends(get_args_list),
):
    if len(args_list) == 0:
        pass
    name = args_list[0]
    if name not in data:
        pass
    if user_block_limiter.check(event.user_id):  # 检查是否在使用
        pass

    path = await get_oxygen_card(name)
    user_block_limiter.set_false(event.user_id)  # 使用完成
