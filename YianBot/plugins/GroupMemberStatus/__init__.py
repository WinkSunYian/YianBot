from nonebot import on_notice
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupIncreaseNoticeEvent
)
from .config import Config
from random import randint

__plugin_name__ = 'GroupMemberStatus'
__plugin_usage__ = '群员数量检测'

# 群成员增加消息响应
GroupIncrease_CS = on_notice(priority=10)


@GroupIncrease_CS.handle()
async def method(bot: Bot, event: GroupIncreaseNoticeEvent):
    group_id = event.group_id  # 获取群号(int)
    group_id = str(group_id)
    if group_id in Config.welcome_speechs.keys():
        if Config.welcome_speechs[group_id] == "default":
            msg = Config.welcome_speechs['default']
        else:
            msg = Config.welcome_speechs[group_id][randint(0, len(Config.welcome_speechs[group_id]))]
    else:
        return
    await bot.send(
        event=event,
        message=msg,
        at_sender=True
    )
