from nonebot import on_notice
from nonebot.adapters.onebot.v11 import (
    Bot,
    Event,
    PokeNotifyEvent,
    MessageSegment
)

from random import choice, randint
from requests import get

pokeme_thesaurus = [
    "qwq",
    "QAQ",
    "阿巴阿巴"
]

poke = on_notice(priority=10)


@poke.handle()
async def poke_handle(bot: Bot, event: PokeNotifyEvent):
    if event.self_id == event.target_id:
        msg = choice(pokeme_thesaurus)
        await poke.finish(MessageSegment.at(event.user_id) + MessageSegment.text(msg))
