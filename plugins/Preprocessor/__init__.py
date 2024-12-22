from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.matcher import matchers, Matcher
from nonebot.message import event_preprocessor, run_preprocessor
from nonebot.exception import IgnoredException
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
    MessageSegment,
    PrivateMessageEvent,
)
from utils.utils import ConfigReader, DailyCountLimiter
from dependencies.get_user_tags import get_user_tags_or_create_user

count = DailyCountLimiter(1)


@event_preprocessor
async def _(event: MessageEvent, state: T_State):
    if event.is_tome():
        tag_list = await get_user_tags_or_create_user(event.user_id)
