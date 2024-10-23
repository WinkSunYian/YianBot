from nonebot import on_command
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    MessageSegment,
    Message,
    MessageEvent,
    PrivateMessageEvent,
)
from nonebot.params import (
    CommandArg
)
from utils.utils import (
    DailyCountLimiter,
    BackpackControl
)
from utils.db_utils import UserBackpackManager
from utils.utils import FreqLimiter, args_split
from random import choice
from .data_source import play

cd = FreqLimiter(60)

robbery = on_command("打劫", aliases={"抢劫"}, priority=6, block=True)


@robbery.handle()
async def _(event: MessageEvent, args: Message = CommandArg()):
    args_list = args_split(args, 1)
    """
    args_list[0] : QQ
    """
    if len(args_list) != 1:
        await robbery.finish(MessageSegment.reply(event.message_id) + "缺少参数[QQ]")
    elif not isinstance(args_list[0], int):
        await robbery.finish(MessageSegment.reply(event.message_id) + "[QQ]应该是一个At对象,或整数")
    elif not (5 <= len(str(args_list[0])) <= 10):
        await robbery.finish(MessageSegment.reply(event.message_id) + "[QQ]的长度为5-10")
    elif args_list[0] == event.user_id:
        await robbery.finish(MessageSegment.reply(event.message_id) + "打劫自己是吧")
    else:
        if cd.check(event.user_id):
            cd.start_cd(event.user_id)
            my_backpack = UserBackpackManager(event.user_id)
            target_backpack = UserBackpackManager(args_list[0])
            money = play(my_backpack["软妹币"], target_backpack["软妹币"])
            if money == 0:
                msg = "打劫路上被叔叔抓走了"
            elif money > 0:
                msg = f"打劫成功,夺取了对方软妹币 * {money}"
                my_backpack["软妹币"] += money
                target_backpack["软妹币"] -= money
            else:
                msg = f"打劫失败,反被对方抢走了 软妹币 * {-money}"
                my_backpack["软妹币"] += money
                target_backpack["软妹币"] -= money
            await robbery.finish(
                MessageSegment.reply(event.message_id) + msg)
        else:
            await robbery.finish(
                MessageSegment.reply(event.message_id) + f"抢劫冷却中,{cd.left_time(event.user_id):.0f}秒")
