from nonebot import on_command
from nonebot.adapters.onebot.v11 import (
    GroupMessageEvent,
    MessageSegment,
)
from utils.http_utils import http_client

signin = on_command("#签到", priority=6, block=True)


@signin.handle()
async def _(event: GroupMessageEvent):
    status, response = await http_client.put(f"/users/{event.user_id}/sign-in")
    await signin.finish(MessageSegment.reply(event.message_id) + response["msg"])
