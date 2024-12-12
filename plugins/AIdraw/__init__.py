from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
    MessageSegment,
    Message
)
from nonebot.params import (
    CommandArg,
    Depends
)
from .data_source import get_draw_link
from utils.utils import (
    UserBlockLimiter,
    BackpackControl,
    Checks
)

__plugin_name__ = 'AIdraw'
__plugin_usage__ = 'AI绘画'

user_block_limiter = UserBlockLimiter()

draw = on_command("#AI绘画", aliases={"#绘画"}, priority=5, block=True)


@draw.handle()
async def draw_handle(event: MessageEvent, args: Message = CommandArg(), config=Depends(Checks)):
    await draw.finish(MessageSegment.reply(event.message_id) + str(config))
    if user_block_limiter.check(event.user_id):  # 检查是否在使用
        await draw.finish(MessageSegment.reply(event.message_id) + "请勿重复发送请求")
    else:
        condition = str(args)
        if condition == " " or not condition:  # 检查参数
            await draw.finish(MessageSegment.reply(event.message_id) + "指令用法:\n#AI绘画 [要素]\n指令别名:\n#绘画")
        else:
            user_block_limiter.set_true(event.user_id)  # 正在使用
            link = await get_draw_link(condition)  # 获取ChatGPT回复
            user_block_limiter.set_false(event.user_id)  # 使用完成

            await draw.finish(MessageSegment.image(link))
