from nonebot import on_command
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    MessageEvent,
    MessageSegment,
    PrivateMessageEvent,
)

from utils.utils import DailyCountLimiter, BackpackControl
from pathlib import Path
from random import choice
from nonebot.plugin import Plugin
from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent
from nonebot.adapters.onebot.v11 import Bot, Event


# class AutoRegisterMeta(type):
#     """
#     元类，用于自动实例化子类并注册触发器
#     """

#     def __new__(cls, name, bases, dct):
#         new_cls = super().__new__(cls, name, bases, dct)
#         if name != "BaseHandler":  # 避免基类被实例化
#             instance = new_cls()  # 自动实例化
#             instance.register()  # 自动注册事件处理器
#         return new_cls


# class BaseHandler(metaclass=AutoRegisterMeta):
#     def __init__(self, trigger):
#         """
#         基类初始化，用于注册事件处理器
#         :param trigger: NoneBot 的事件触发器（如 on_fullmatch 等）
#         """
#         self.trigger = trigger

#     def register(self):
#         """
#         注册事件处理器到触发器
#         """

#         @self.trigger.handle()
#         async def handle_event(bot: Bot, event: Event):
#             await self.func(bot, event)

#     async def func(self, bot: Bot, event: Event):
#         """
#         子类需要实现的功能逻辑
#         """
#         raise NotImplementedError("子类必须实现 func 方法")


# class TestHandler(BaseHandler):
#     def __init__(self):
#         # 定义触发器，如 on_fullmatch
#         trigger = on_fullmatch("#test", priority=6, block=True)
#         super().__init__(trigger)

#     async def func(self, bot: Bot, event: GroupMessageEvent):
#         # 实现具体的功能逻辑
#         await self.trigger.finish("你好")


test = on_command("#test", priority=6, block=True)


@test.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    result = await bot.call_api(
        "get_group_msg_history",
        group_id=event.group_id,
        count=5,
    )

    messages = result["data"]
    if not messages:
        await test.finish("没有找到历史消息。")
        return

    history_text = ""
    for msg in messages:
        user_id = msg.get("user_id", "未知用户")
        content = msg.get("message", "[无法解析]")
        history_text += f"{user_id}: {content}\n"

    await test.finish(history_text)
