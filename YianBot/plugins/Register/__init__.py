from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.message import event_preprocessor
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    PrivateMessageEvent,
    Message,
    MessageEvent
)
from utils.db_utils import get_user


@event_preprocessor
async def _(event: MessageEvent):
    if event.is_tome():
        get_user(user_id=event.user_id)
