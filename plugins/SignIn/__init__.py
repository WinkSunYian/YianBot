from nonebot import on_fullmatch
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    MessageSegment,
    PrivateMessageEvent,
)
from utils.http_utils import http_client

signin = on_fullmatch("签到", priority=6, block=True)


@signin.handle()
async def _(event: GroupMessageEvent):
    status, response = await http_client.put(f"/users/{event.user_id}/chat-ai")
    await signin.finish(MessageSegment.reply(event.message_id) + response["msg"])
