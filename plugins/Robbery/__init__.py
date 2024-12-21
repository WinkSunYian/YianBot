from nonebot import on_command
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    MessageSegment,
    Message,
    MessageEvent,
    PrivateMessageEvent,
)
from nonebot.params import CommandArg
from random import choice
from utils.utils import DailyCountLimiter, BackpackControl
from utils.utils import FreqLimiter, args_split
from utils.http_utils import http_client

cd = FreqLimiter(60)

robbery = on_command("打劫", aliases={"抢劫"}, priority=6, block=True)


@robbery.handle()
async def _(event: MessageEvent, args: Message = CommandArg()):
    print(args)
    args_list = args_split(args, 1)
    print(args_list)
    """
    args_list[0] : QQ
    """
    if len(args_list) != 1:
        await robbery.finish(MessageSegment.reply(event.message_id) + "缺少参数[QQ]")
    elif not isinstance(args_list[0], int):
        await robbery.finish(
            MessageSegment.reply(event.message_id) + "[QQ]应该是一个At对象,或整数"
        )
    elif not (5 <= len(str(args_list[0])) <= 10):
        await robbery.finish(
            MessageSegment.reply(event.message_id) + "[QQ]的长度为5-10"
        )
    elif args_list[0] == event.user_id:
        await robbery.finish(MessageSegment.reply(event.message_id) + "打劫自己是吧")
    else:
        if cd.check(event.user_id):
            cd.start_cd(event.user_id)
            print(event.user_id, args_list)
            status, response = await http_client.post(
                f"/users/{event.user_id}/robbery", json={"target_id": args_list[0]}
            )
            await robbery.finish(
                MessageSegment.reply(event.message_id) + response["msg"]
            )
        else:
            await robbery.finish(
                MessageSegment.reply(event.message_id)
                + f"抢劫冷却中,{cd.left_time(event.user_id):.0f}秒"
            )
