from nonebot import on_command
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
    MessageSegment
)
from .data_source import get_luck

__plugin_name__ = 'TodayLuck'
__plugin_usage__ = '今日运势'

luck = on_command("今日运势", priority=6, block=True)


@luck.handle()
async def luck_handle(event: MessageEvent):
    msg = get_luck(event.user_id)
    await luck.finish(MessageSegment.reply(event.message_id) + f"{msg}")
