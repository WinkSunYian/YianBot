from nonebot import on_command
from nonebot.params import Depends
from nonebot.adapters.onebot.v11 import (
    GroupMessageEvent,
    MessageSegment,
)
from utils.http_utils import http_client
from dependencies.get_user_tags import get_user_tags

signin = on_command("#签到", aliases={"签到"}, priority=6, block=True)


@signin.handle()
async def _(event: GroupMessageEvent, tags: list = Depends(get_user_tags)):
    status, response = await http_client.put(f"/users/{event.user_id}/sign-in")
    await signin.finish(MessageSegment.reply(event.message_id) + response["message"])
