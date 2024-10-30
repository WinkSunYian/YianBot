from nonebot import on_notice
from nonebot.adapters.onebot.v11 import (
    Bot,
    Event,
    LuckyKingNotifyEvent,
    MessageSegment
)


__plugin_name__ = 'LuckyKing'
__plugin_usage__ = '运气王'

luck = on_notice(priority=10)


@luck.handle()
async def fun(bot: Bot, event: LuckyKingNotifyEvent):
    atmsg = MessageSegment.at(event.target_id)
    msg = "运气王:" + atmsg
    await luck.finish(msg)