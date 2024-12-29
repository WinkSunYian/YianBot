from nonebot import on_command
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
    Message,
)
from nonebot.params import CommandArg
from configs.Config import MASTER

__plugin_name__ = "ChatAI"
__plugin_usage__ = "Echo"


echo = on_command("#echo", priority=5, block=True)


@echo.handle()
async def ban_handle(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    if event.user_id == MASTER:
        await echo.finish(str(args))
