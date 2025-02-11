from nonebot import on_message, on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    PrivateMessageEvent,
    MessageSegment,
)
from .data_source import (
    getChat,
)
from utils.utils import BanCheckLimiter
from .data_source import getChatAIresponse

__plugin_name__ = "ChatAI"
__plugin_usage__ = "聊天AI"

private_chat = on_message(priority=10, block=False)
group_chat = on_message(priority=10, rule=to_me(), block=False)


@private_chat.handle()
async def _(bot: Bot, event: PrivateMessageEvent):
    pass


@group_chat.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    if event.user_id == 2854196310:  # 是否为Q群管家
        return

    result = await bot.call_api(
        "get_group_msg_history",
        group_id=event.group_id,
        count=10,
    )
    response = await getChatAIresponse(result, event.user_id)
    await group_chat.finish(response)


# banCheckLimiter = BanCheckLimiter()

# chat = on_message(priority=10)


# @chat.handle()
# async def chat_handle(event: MessageEvent):
#     if event.user_id == 2854196310:  # 是否为Q群管家
#         return

#     at = event.is_tome() and event.user_id != event.self_id  # 是否at了bot

#     if at and banCheckLimiter.check(event.user_id):
#         await chat.finish("恶意请求")
#     banCheckLimiter.add(event.user_id)

#     msg = await getChat(
#         event.message.extract_plain_text(), at=at, user_id=event.user_id
#     )

#     if msg:  # 如果消息不为空
#         await chat.finish(msg)
