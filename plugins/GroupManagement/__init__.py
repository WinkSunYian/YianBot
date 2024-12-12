from nonebot import (
    on_command
)
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    Message,
    MessageSegment
)
from nonebot.params import CommandArg
from utils.utils import args_split
from configs.Config import MASTER, NICKNAME

__plugin_name__ = 'GroupManagement'
__plugin_usage__ = '群管'

set_ban = on_command("#禁言", priority=10, block=True)


@set_ban.handle()
async def set_ban_handle(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    self_role = (await bot.get_group_member_info(
        group_id=event.group_id,
        user_id=event.self_id
    ))['role']

    if self_role in ['admin', 'owner']:
        if event.sender.role in ['admin', 'owner'] or event.user_id == MASTER:
            args_list = args_split(args, 2, [int, int])
            """
            args_lsit[0]: QQ号
            args_lsit[1]: 禁言时长
            """
            if len(args_list) != 2:
                await set_ban.finish(
                    MessageSegment.reply(event.message_id) + "指令用法:\n#禁言 [QQ号] [禁言时长]\n[禁言时长单位为秒,不支持单位换算]")
            elif args_list[0] == MASTER:
                await set_ban.finish(MessageSegment.reply(event.message_id) + "nonono")
            else:
                await bot.set_group_ban(
                    group_id=event.group_id,
                    user_id=args_list[0],
                    duration=args_list[1]
                )
                await set_ban.finish(MessageSegment.reply(event.message_id) + f"{args_list[0]}不听话,被我禁言了{args_list[1]}秒")
        else:
            await bot.set_group_ban(
                group_id=event.group_id,
                user_id=event.sender.user_id,
                duration=600
            )
            await set_ban.finish(MessageSegment.reply(event.message_id) + "你在教我做事?")
    else:
        await set_ban.finish(MessageSegment.reply(event.message_id) + f"{NICKNAME}没有这个权限呢")


unset_ban = on_command("#解除禁言", aliases={"#解禁"}, priority=10, block=True)


@unset_ban.handle()
async def unset_ban_handle(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    self_role = (await bot.get_group_member_info(
        group_id=event.group_id,
        user_id=event.self_id
    ))['role']

    if self_role in ['admin', 'owner']:
        if event.sender.role in ['admin', 'owner'] or event.user_id == MASTER:
            args_list = args_split(args, 1)
            if len(args_list) != 1:
                await unset_ban.finish(MessageSegment.reply(event.message_id) + "指令用法:\n#解除禁言 [QQ号]\n指令别名:\n#解禁")
            else:
                await bot.set_group_ban(
                    group_id=event.group_id,
                    user_id=args_list[0],
                    duration=0
                )
                await unset_ban.finish(MessageSegment.reply(event.message_id) + f"{args_list[0]}已被解除禁言")
        else:
            await bot.set_group_ban(
                group_id=event.group_id,
                user_id=event.sender.user_id,
                duration=600
            )
            await unset_ban.finish(MessageSegment.reply(event.message_id) + "我是你能命令的吗?")
    else:
        await unset_ban.finish(MessageSegment.reply(event.message_id) + f"{NICKNAME}权限不够呢")


kick = on_command("#踢", priority=10, block=True)


@kick.handle()
async def kick_handle(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    self_role = (await bot.get_group_member_info(
        group_id=event.group_id,
        user_id=event.self_id
    ))['role']

    if self_role in ['admin', 'owner']:
        if event.sender.role in ['admin', 'owner'] or event.user_id == MASTER:
            args_list = args_split(args, 1)
            if len(args_list) != 1:
                await kick.finish(MessageSegment.reply(event.message_id) + "指令用法:\n#踢 [qq]")
            elif args_list[0] == MASTER:
                await kick.finish(MessageSegment.reply(event.message_id) + "nonono")
            else:
                await bot.set_group_kick(
                    group_id=event.group_id,
                    user_id=args_list[0],
                    reject_add_request=False  # 是否拉黑
                )
                await kick.finish(MessageSegment.reply(event.message_id) + f"{args_list[0]}被我踢啦")
        else:
            await bot.set_group_ban(
                group_id=event.group_id,
                user_id=event.sender.user_id,
                duration=600
            )
            await unset_ban.finish(MessageSegment.reply(event.message_id) + "我是你能命令的吗?")
    else:
        await unset_ban.finish(MessageSegment.reply(event.message_id) + f"{NICKNAME}权限不够呢")
