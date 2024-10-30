from nonebot import on_fullmatch
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    MessageSegment,
    PrivateMessageEvent,
)

from utils.utils import (
    DailyCountLimiter,
    BackpackControl
)

from random import choice

# 签到奖励
reward = {
    "软糖": [i for i in range(1, 10)],
    "小熊饼干": [0 for i in range(0, 5)] + [1],
    "软妹币": [i for i in range(0, 50)],
}

count = DailyCountLimiter(1)

signin = on_fullmatch("签到", priority=6, block=True)


@signin.handle()
async def _(event: GroupMessageEvent):
    if count.check(event.user_id):
        count.increase(event.user_id)
        backpack = UserBackpackManager(event.user_id)
        msg = choice([
            "签到成功,获得了:",
            "签到成功,获得奖励:"
        ])
        for item in reward.keys():
            quantity = choice(reward[item])
            if quantity == 0:
                continue
            msg += "\n{} * {}".format(item, quantity)
            backpack[item] += quantity

        await signin.finish(
            MessageSegment.reply(event.message_id) + msg)

    else:
        await signin.finish(MessageSegment.reply(event.message_id) + "您今天已经签过到了")
