from nonebot import on_command
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
)
from .data_source import get_love_talk

love = on_command("#情话", priority=5, block=True)


@love.handle()
async def _(bot: Bot, event: MessageEvent):
    msg = await get_love_talk()
    await love.finish(msg)
