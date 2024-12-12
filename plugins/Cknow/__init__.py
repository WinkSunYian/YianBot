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
from .data_source import get_cknows_answer
from utils.utils import (
    UserBlockLimiter,
    BackpackControl
)

user_block_limiter = UserBlockLimiter()

gpt = on_command("#C知道", aliases={"#cn", "#Cknow"}, priority=5, block=True)


@gpt.handle()
async def gpt_handle(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    if user_block_limiter.check(event.user_id):  # 检查是否在使用
        await gpt.finish(MessageSegment.reply(event.message_id) + "请勿重复发送请求")
    else:
        question = str(args)
        if question == " " or not question:  # 检查参数
            await gpt.finish(MessageSegment.reply(event.message_id) + "指令用法:\n#Cknow [问题]\n指令别名:\n#cn,#C知道")
        else:
            user_block_limiter.set_true(event.user_id)  # 正在使用
            answer = await get_cknows_answer(question)  # 获取Cknow回复
            user_block_limiter.set_false(event.user_id)  # 使用完成
            await gpt.finish(MessageSegment.reply(event.message_id) + answer)
