from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.matcher import matchers, Matcher
from nonebot.message import event_preprocessor, run_preprocessor
from nonebot.exception import IgnoredException
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
async def _(bot: Bot, event: PrivateMessageEvent):
    if count.check(event.user_id):
        count.increase(event.user_id)
        await bot.send(
            event=event,
            message="广告内容",
        )


@event_preprocessor
async def _(event: MessageEvent):
    if event.is_tome():
        tag_list = await get_user_tags_or_create(event.user_id)
        # if is_tag_present(tag_list, "banned"):
        # raise IgnoredException("黑名单用户")


@run_preprocessor
async def _(bot: Bot, event: MessageEvent, matcher: Matcher):
    if event.is_tome():
        config = ConfigReader(matcher.plugin.name)
        if config["plugin"] == "disable":
            if config["disableReason"] != "":
                await bot.send(
                    event=event,
                    message=MessageSegment.reply(event.message_id)
                    + config["disableReason"],
                )
                raise IgnoredException("插件被禁用")
