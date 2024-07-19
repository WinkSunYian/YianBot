from nonebot import on_command
from nonebot.adapters.onebot.v11 import (
    Bot,
    Message,
    PrivateMessageEvent,
    MessageEvent,
    MessageSegment
)
from nonebot.params import CommandArg
from .data_source import pay_kuai3
from utils.utils import (
    BackpackControl,
    args_split
)


def arg_check(arg):
    for i in arg:
        if i not in ["大", "小", "单", "双"]:
            return False
    else:
        return True


buy = on_command("#ks", priority=5, block=True)


@buy.handle()
async def buy_handle(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    args_list = args_split(args, 2)
    """
    args_list[0] : 购买内容
    args_list[1.yml] : 金额
    """
    if len(args_list) != 2:
        await buy.finish(
            MessageSegment.reply(event.message_id) + "指令用法:\n#ks {购买内容} [每注金额]\n[购买内容]:{大,小,单,双}")
    elif not arg_check(args_list[0]):
        await buy.finish(
            MessageSegment.reply(event.message_id) + "你他妈会不会玩？")
    elif args_list[1] < 10:
        await buy.finish(
            MessageSegment.reply(event.message_id) + "[每注金额]必须为整数且大于10")
    else:
        # play
        backpack = BackpackControl(event.user_id)
        if backpack['软妹币'] < args_list[1]:
            await buy.finish(
                MessageSegment.reply(event.message_id) + "你没有足够的软妹币")
        else:
            result = pay_kuai3(args_list[0], args_list[1])
            backpack['软妹币'] = round(
                backpack['软妹币'] + (result['money'] - (len(args_list[0]) * args_list[1])), 2)
            msg = f"[{result['a']},{result['b']},{result['c']}] [{result['total']},{result['big_or_small']},{result['odd_or_even']}]\n"
            msg += f"买入 {args_list[0]} * {args_list[1]}\n奖金: {result['money']}\n余额:{backpack['软妹币']}"
            backpack.save()
            await buy.finish(
                MessageSegment.reply(event.message_id) + msg)
