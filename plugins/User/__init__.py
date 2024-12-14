from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, Message, MessageSegment
from nonebot.params import CommandArg
from utils.utils import args_split
from utils.utils import FreqLimiter
from utils.http_utils import http_client
from configs.Config import MASTER

__plugin_name__ = "User"
__plugin_usage__ = "用户"

cd = FreqLimiter(60)


def beautify_data(item_list):
    msg = "┏" + "━" * 10 + "\n"
    for item in item_list:
        msg += f"┃ {item['name']} x {item['quantity']}\n"
    else:
        msg += "┃ 空空如也\n"
    msg += "┗" + "━" * 10
    return msg


mypack = on_command("#背包", priority=5, block=True)


@mypack.handle()
async def mypack_handle(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    args_list = args_split(args, 1)
    status, response = await http_client.put(f"/api/users/{event.user_id}/items")
    item_list = response["data"]
    await mypack.finish(
        MessageSegment.reply(event.message_id) + beautify_data(item_list)
    )


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
            MessageSegment.reply(event.message_id)
            + "指令用法:\n#转账 [QQ] [物品名称] [数量]"
        )
    elif not isinstance(args_list[0], int):
        await transfer.finish(MessageSegment.reply(event.message_id) + "你要转给谁?")
    elif args_list[0] == event.user_id:
        await transfer.finish(MessageSegment.reply(event.message_id) + "自我转账?")
    elif not isinstance(args_list[2], int):
        await transfer.finish(
            MessageSegment.reply(event.message_id) + "[数量]必须为整数"
        )
    elif args_list[2] < 0:
        await transfer.finish(
            MessageSegment.reply(event.message_id) + "[数量]必须大于0"
        )
    else:
        if cd.check(event.user_id):
            cd.start_cd(event.user_id)
            my_backpack = UserBackpackManager(event.user_id)
            target_backpack = UserBackpackManager(args_list[0])
            if my_backpack[args_list[1]] >= args_list[2]:
                my_backpack[args_list[1]] -= args_list[2]
                target_backpack[args_list[1]] += args_list[2]
                await transfer.finish(
                    MessageSegment.reply(event.message_id)
                    + f"成功向{args_list[0]}转账了{args_list[1]} * {args_list[2]}"
                )
            else:
                await transfer.finish(
                    MessageSegment.reply(event.message_id)
                    + f"你没有足够多的{args_list[1]}"
                )
        else:
            await transfer.finish(
                MessageSegment.reply(event.message_id)
                + f"冷却{cd.left_time(event.user_id):.0f}"
            )
