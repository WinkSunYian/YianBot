from nonebot import on_fullmatch
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageSegment,
    MessageEvent
)

from utils.utils import args_split, ConfigReader
import os

help = on_fullmatch("菜单", priority=5, block=True)


@help.handle()
async def _(event: MessageEvent):
    msg_list = []
    for plugin in os.listdir("plugins/"):
        if "_" in plugin:
            continue
        config = ConfigReader(plugin)
        if "commands" in config:
            for command in config["commands"]:
                msg_list.append(command)
    await help.finish(MessageSegment.reply(event.message_id) + "\n".join(msg_list))
