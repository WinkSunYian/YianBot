from nonebot import on_command
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
    MessageSegment,
    Message
)
from nonebot.params import (
    CommandArg
)
from utils.utils import (
    args_split
)
from .data_source import get_card

__plugin_name__ = 'licensing'
__plugin_usage__ = '发牌'

_ = on_command("#发牌", priority=5, block=True)


@_.handle()
async def __(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    args_list = args_split(args, 1)
    """
    args_list[0] : 卡牌数量
    """
    if len(args_list) == 0:
        args_list.append(1)
    if args_list[0] >= 6:
        args_list[0] = 6

    await _.finish(MessageSegment.image("file:///" + get_card(args_list[0])))
