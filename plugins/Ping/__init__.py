from nonebot import on_command
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
    Message,
    MessageSegment
)
from nonebot.params import CommandArg
from utils.utils import args_split
from .data_source import get_ping

test = on_command("#ping", priority=5, block=True)


@test.handle()
async def test_handle(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    args_list = args_split(args, 1)
    """
    args_list[0] : 目标网站
    """
    msg = await get_ping(args_list[0])
    await test.finish(MessageSegment.reply(event.message_id) + msg)
