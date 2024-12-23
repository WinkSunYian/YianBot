from nonebot import on_request
from nonebot.adapters.onebot.v11 import Bot, FriendRequestEvent, GroupRequestEvent
from utils.utils import DailyCountLimiter
from configs.Config import MASTER
import asyncio
from random import randint

count = DailyCountLimiter(5)

__plugin_name__ = "SetRequest"
__plugin_usage__ = "处理请求"

friend = on_request(priority=6, block=True)


@friend.handle()
async def friend_handle(bot: Bot, event: FriendRequestEvent):
    await bot.send_msg(
        message_type="private",
        # 私聊用户QQ号
        user_id=MASTER,
        message=f"收到{event.user_id}的好友请求",
    )
    if count.check(1):
        count.increase(1)
        await asyncio.sleep(randint(2, 5))
        await event.approve(bot=bot)
        await bot.send_msg(
            message_type="private",
            # 私聊用户QQ号
            user_id=MASTER,
            message=f"已添加{event.user_id}为好友",
        )


group = on_request(priority=6, block=True)


@group.handle()
async def group_handle(bot: Bot, event: GroupRequestEvent):
    print(event.sub_type)
    if event.sub_type == "invite":
        await bot.send_msg(
            message_type="private",
            # 私聊用户QQ号
            user_id=MASTER,
            message=f"收到{event.user_id}的{event.group_id}入群邀请",
        )
        if count.check(1):
            count.increase(1)
            await asyncio.sleep(randint(2, 5))
            await event.approve(bot)
            await bot.send_msg(
                message_type="private",
                # 私聊用户QQ号
                user_id=MASTER,
                message=f"已同意{event.user_id}的{event.group_id}入群邀请",
            )
            await bot.send_msg(
                message_type="private",
                # 私聊用户QQ号
                user_id=event.user_id,
                message=f"我已同意进入{event.group_id}",
            )
        else:
            await bot.send_msg(
                message_type="private",
                # 私聊用户QQ号
                user_id=event.user_id,
                message="今日处理申请已达上限,明天再来吧",
            )
