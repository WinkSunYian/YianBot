from nonebot import on_command
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
    MessageSegment,
    Message,
)
from nonebot.params import (
    CommandArg
)
from .data_source import (
    get_touch_link,
    get_pound_link,
    get_bite_link,
    get_misfortune_link,
    get_ding_link,
    get_tietie_link,
    get_luxun_link
)
from utils.utils import (
    args_split,
    UserBlockLimiter,
    is_number
)

user_block_limiter = UserBlockLimiter()

touchlt = on_command("摸", priority=5, block=True)


@touchlt.handle()
async def _touchlt(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    if user_block_limiter.check(event.user_id):  # 检查是否在使用
        pass

    user_block_limiter.set_true(event.user_id)  # 正在使用
    args_list = args_split(args, 1)
    if len(args_list) != 1:
        pass
    elif not is_number(args_list[0]):
        pass
    else:
        link = await get_touch_link(args_list[0])
        user_block_limiter.set_false(event.user_id)  # 使用完成
        await touchlt.finish(MessageSegment.image(link))


pound = on_command("砸", priority=5, block=True)


@pound.handle()
async def _pound(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    if user_block_limiter.check(event.user_id):  # 检查是否在使用
        pass
    user_block_limiter.set_true(event.user_id)  # 正在使用
    args_list = args_split(args, 1)
    if len(args_list) != 1:
        pass
    elif not is_number(args_list[0]):
        pass
    else:
        link = await get_pound_link(args_list[0])
        user_block_limiter.set_false(event.user_id)
        await pound.finish(MessageSegment.image(link))


bite = on_command("吃", priority=5, block=True)


@bite.handle()
async def _bite(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    if user_block_limiter.check(event.user_id):  # 检查是否在使用
        pass

    user_block_limiter.set_true(event.user_id)  # 正在使用
    args_list = args_split(args, 1)
    if len(args_list) != 1:
        pass
    elif not is_number(args_list[0]):
        pass
    else:
        link = await get_bite_link(args_list[0])
        user_block_limiter.set_false(event.user_id)  # 使用完成
        await bite.finish(MessageSegment.image(link))


misfortune = on_command("不幸", priority=5, block=True)


@misfortune.handle()
async def _misfortune(event: MessageEvent, args: Message = CommandArg()):
    if user_block_limiter.check(event.user_id):  # 检查是否在使用
        pass
    user_block_limiter.set_true(event.user_id)  # 正在使用
    args_list = args_split(args, 1)
    if len(args_list) != 1:
        pass
    elif not is_number(args_list[0]):
        pass
    else:
        link = await get_misfortune_link(args_list[0])
        user_block_limiter.set_false(event.user_id)  # 使用完成
        await misfortune.finish(MessageSegment.image(link))


tietie = on_command("贴贴", priority=5, block=True)


@tietie.handle()
async def _tietie(event: MessageEvent, args: Message = CommandArg()):
    if user_block_limiter.check(event.user_id):  # 检查是否在使用
        pass

    user_block_limiter.set_true(event.user_id)  # 正在使用
    args_list = args_split(args, 1)
    if len(args_list) != 1:
        pass
    elif not is_number(args_list[0]):
        pass
    else:
        link = await get_tietie_link(args_list[0])
        user_block_limiter.set_false(event.user_id)  # 使用完成
        await tietie.finish(MessageSegment.image(link))


ding = on_command("顶", priority=5, block=True)


@ding.handle()
async def _ding(event: MessageEvent, args: Message = CommandArg()):
    if user_block_limiter.check(event.user_id):  # 检查是否在使用
        pass

    user_block_limiter.set_true(event.user_id)  # 正在使用
    args_list = args_split(args, 1)
    if len(args_list) != 1:
        pass
    elif not is_number(args_list[0]):
        pass
    else:
        link = await get_ding_link(args_list[0])
        user_block_limiter.set_false(event.user_id)  # 使用完成
        await ding.finish(MessageSegment.image(link))


luxun = on_command("鲁迅说", priority=5, block=True)


@luxun.handle()
async def _luxun(event: MessageEvent, args: Message = CommandArg()):
    if user_block_limiter.check(event.user_id):  # 检查是否在使用
        pass
    user_block_limiter.set_true(event.user_id)  # 正在使用
    args_list = args_split(args, 1)
    if len(args_list) != 1:
        pass
    elif not is_number(args_list[0]):
        pass
    else:
        link = await get_luxun_link(args_list[0])
        user_block_limiter.set_false(event.user_id)  # 使用完成
        await luxun.finish(MessageSegment.image(link))
