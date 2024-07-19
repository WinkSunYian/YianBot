from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.matcher import matchers, Matcher
from nonebot.message import event_preprocessor, run_preprocessor
from nonebot.exception import IgnoredException
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    PrivateMessageEvent,
    Message,
    MessageEvent,
    MessageSegment
)
from utils.db_utils import get_user
from utils.utils import ConfigReader


@event_preprocessor
async def _(event: MessageEvent):
    if event.is_tome():
        get_user(user_id=event.user_id)


@run_preprocessor
async def _(bot: Bot, event: MessageEvent, matcher: Matcher):
    if event.user_id != 7345222:
        config = ConfigReader(matcher.plugin.name)
        if config["plugin"] == "disable":
            if config["disableReason"] != "":
                await bot.send(
                    event=event,
                    message=MessageSegment.reply(event.message_id) + config["disableReason"]
                )
                raise IgnoredException("插件被禁用")
