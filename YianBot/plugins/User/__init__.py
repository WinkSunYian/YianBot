from nonebot import on_command
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
    Message,
    MessageSegment
)
from nonebot.params import (
    CommandArg
)
from utils.utils import (
    BackpackControl,
    args_split
)

from utils.db_utils import (
    UserBackpackManager
)
from configs.configs import MASTER
from .data_source import (
    construct
)

__plugin_name__ = 'User'
__plugin_usage__ = '用户'

mypack = on_command("#背包", priority=5, block=True)


@mypack.handle()
async def mypack_handle(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    if event.user_id == MASTER:
        args_list = args_split(args, 1)
        if len(args_list) == 0:
            args_list.append(event.user_id)
        backpack = UserBackpackManager(args_list[0])
        await mypack.finish(MessageSegment.reply(event.message_id) + construct(backpack))
    else:
        backpack = UserBackpackManager(event.user_id)
        await mypack.finish(MessageSegment.reply(event.message_id) + construct(backpack))


transfer = on_command("#转账", priority=5, block=True)


@transfer.handle()
async def transfer_handle(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    args_list = args_split(args, 3)
    """
    args_list[0] : QQ
    args_list[1] : 物品名称
    args_list[2] : 数量
    """
    if len(args_list) != 3:
        await transfer.finish(
            MessageSegment.reply(event.message_id) + "指令用法:\n#转账 [QQ] [物品名称] [数量]")
    elif not isinstance(args_list[0], int):
        await transfer.finish(
            MessageSegment.reply(event.message_id) + "你要转给谁?")
    elif args_list[0] == event.user_id:
        await transfer.finish(
            MessageSegment.reply(event.message_id) + "自我转账?")
    elif not isinstance(args_list[2], int):
        await transfer.finish(
            MessageSegment.reply(event.message_id) + "[数量]必须为整数")
    elif args_list[2] < 0:
        await transfer.finish(
            MessageSegment.reply(event.message_id) + "[数量]必须大于0")
    else:
        my_backpack = BackpackControl(event.user_id)
        target_backpack = BackpackControl(args_list[0])
        if not my_backpack.use_item(args_list[1], args_list[2]):
            target_backpack.get_item(args_list[1], args_list[2])
            await transfer.finish(
                MessageSegment.reply(event.message_id) +
                f"成功向{args_list[0]}转账了{args_list[1]} * {args_list[2]}")
        else:
            await transfer.finish(
                MessageSegment.reply(event.message_id) + f"你没有足够多的{args_list[1]}")
