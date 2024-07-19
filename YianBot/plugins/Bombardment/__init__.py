from nonebot import on_command
from nonebot.adapters.onebot.v11 import (
    Bot,
    Message,
    MessageEvent,
    MessageSegment
)
from nonebot.params import (
    CommandArg,
    Depends
)

from random import (
    randint
)
from utils.utils import (
    BackpackControl,
    args_split,
    Checks
)
from .data_source import submitBombingRequest


disable_phone = [
    "15656561576"
]

bombardment = on_command("#短轰", priority=5, block=True)


@bombardment.handle()
async def _(bot: Bot, event: MessageEvent, args: Message = CommandArg(),res = Depends(Checks)):
    args_list = args_split(args, 2)
    """
    args_list[0] : 手机号
    args_list[1] : 时长分钟
    """
    if len(args_list) != 2:
        await bombardment.finish(
            MessageSegment.reply(
                event.message_id) + "指令用法:\n#短轰 [手机号] [时长分钟]\n消耗:\n方糖 * [时长分钟]\n[时长分钟]为服务器提交时长,并非[手机号]收到短信时长")
    elif len(str(args_list[0])) != 11:
        await bombardment.finish(
            MessageSegment.reply(event.message_id) + "[手机号]的长度应该为11")
    else:
        backpack = BackpackControl(event.user_id)
        if backpack['方糖'] >= args_list[1]:
            code, msg = await submitBombingRequest(args_list[0], args_list[1])
            if code == 0:
                backpack['方糖'] -= args_list[1]
                backpack.save()
                await bombardment.finish(
                    MessageSegment.reply(event.message_id) + msg)
            else:
                await bombardment.finish(
                    MessageSegment.reply(event.message_id) + msg)
        else:
            await bot.send(
                event=event,
                message="\n方糖不够了嗷\n使用 #背包 指令查看自己的背包",
                at_sender=True
            )
            if randint(0, 5) == 0:
                await bombardment.finish(MessageSegment.reply(event.message_id) +
                                         "方糖获取方法:\n在VIP群签到(白嫖)\n购买(巨便宜)\n具体联系Q7345222")
