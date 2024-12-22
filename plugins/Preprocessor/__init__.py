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
from .data_source import get_user_tags, is_tag_present, get_user_tags_or_create

count = DailyCountLimiter(1)


@event_preprocessor
async def _(event: MessageEvent, state: T_State):
    if event.is_tome():
        tag_list = await get_user_tags_or_create(event.user_id)
