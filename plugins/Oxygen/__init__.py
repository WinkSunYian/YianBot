from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment, Message
from nonebot.params import CommandArg, Depends
from .data_source import get_oxygen_card
from utils.utils import UserBlockLimiter
from dependencies.get_args_list import get_args_list

user_block_limiter = UserBlockLimiter()


qy = on_command("#缺氧", aliases={"缺氧"}, priority=6, block=True)


@qy.handle()
async def _(
    bot: Bot,
    event: MessageEvent,
    args_list: list = Depends(get_args_list),
):
    if len(args_list) == 0:
        return
    name = args_list[0]
    if user_block_limiter.check(event.user_id):
        return

    path = await get_oxygen_card(name)
    if not path:
        return
    with open(path, "rb") as f:
        image_bytes = f.read()
    user_block_limiter.set_false(event.user_id)
    await qy.finish(MessageSegment.image(image_bytes))
